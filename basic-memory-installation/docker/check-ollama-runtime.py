#!/usr/bin/env python3
"""Inventory Ollama libraries and check CUDA 12.8 without starting a service or model."""
import ctypes as c
import json
import os
from pathlib import Path
import re
import subprocess

root=Path('/usr/lib/ollama')
assert root.is_dir(),'The Ollama runtime library folder is absent.'
libraries=[]
for path in sorted(root.rglob('*')):
    if '.so' not in path.name or not (path.is_file() or path.is_symlink()):continue
    libraries.append({'path':str(path),'resolved_path':str(path.resolve()),'bytes':path.stat().st_size,
        'filename_version':path.name.split('.so.',1)[1] if '.so.' in path.name else None,
        'symlink':path.is_symlink()})
cuda12=sorted({path.resolve() for path in root.rglob('libcudart.so*') if '/cuda_v12/' in str(path)})
assert len(cuda12)==1,('Expected one distinct CUDA 12 runtime',list(map(str,cuda12)))
runtime=c.CDLL(str(cuda12[0]),mode=c.RTLD_GLOBAL)
def check(function,*arguments):
    status=function(*arguments)
    if status!=0:raise RuntimeError(function.__name__+' returned status '+str(status))
version=c.c_int();runtime.cudaRuntimeGetVersion.argtypes=[c.POINTER(c.c_int)]
check(runtime.cudaRuntimeGetVersion,c.byref(version))
assert version.value==12080,('Expected CUDA 12.8',version.value)
count=c.c_int();runtime.cudaGetDeviceCount.argtypes=[c.POINTER(c.c_int)]
check(runtime.cudaGetDeviceCount,c.byref(count));assert count.value>=1
runtime.cudaSetDevice.argtypes=[c.c_int];check(runtime.cudaSetDevice,0)
pointer=c.c_void_p();runtime.cudaMalloc.argtypes=[c.POINTER(c.c_void_p),c.c_size_t]
runtime.cudaMemset.argtypes=[c.c_void_p,c.c_int,c.c_size_t]
runtime.cudaMemcpy.argtypes=[c.c_void_p,c.c_void_p,c.c_size_t,c.c_int]
runtime.cudaFree.argtypes=[c.c_void_p]
check(runtime.cudaMalloc,c.byref(pointer),32)
try:
    check(runtime.cudaMemset,pointer,0x5a,32)
    host=(c.c_ubyte*32)()
    check(runtime.cudaMemcpy,c.cast(host,c.c_void_p),pointer,32,2)
    assert bytes(host)==b'Z'*32,'CUDA memory round trip differs.'
finally:check(runtime.cudaFree,pointer)
driver=c.CDLL('libcuda.so.1');driver.cuInit.argtypes=[c.c_uint];check(driver.cuInit,0)
device=c.c_int();driver.cuDeviceGet.argtypes=[c.POINTER(c.c_int),c.c_int];check(driver.cuDeviceGet,c.byref(device),0)
device_name=c.create_string_buffer(256);driver.cuDeviceGetName.argtypes=[c.c_void_p,c.c_int,c.c_int]
check(driver.cuDeviceGetName,device_name,256,device)
major=c.c_int();minor=c.c_int();driver.cuDeviceComputeCapability.argtypes=[c.POINTER(c.c_int),c.POINTER(c.c_int),c.c_int]
check(driver.cuDeviceComputeCapability,c.byref(major),c.byref(minor),device)
assert '5090' in device_name.value.decode(),device_name.value
assert (major.value,minor.value)==(12,0),(major.value,minor.value)
# Read cuBLAS's actual library version from a handle, then release it immediately.
cublas_paths=sorted({path.resolve() for path in root.rglob('libcublas.so*') if '/cuda_v12/' in str(path)})
assert len(cublas_paths)==1,cublas_paths
blas=c.CDLL(str(cublas_paths[0]));handle=c.c_void_p()
blas.cublasCreate_v2.argtypes=[c.POINTER(c.c_void_p)];check(blas.cublasCreate_v2,c.byref(handle))
blas.cublasGetVersion_v2.argtypes=[c.c_void_p,c.POINTER(c.c_int)];blas.cublasDestroy_v2.argtypes=[c.c_void_p]
blas_version=c.c_int()
try:
    check(blas.cublasGetVersion_v2,handle,c.byref(blas_version))
    # Execute a 1-by-1 matrix multiplication to verify a real cuBLAS GPU kernel.
    values=(c.c_float*3)(2.0,3.0,0.0);gpu_values=c.c_void_p()
    check(runtime.cudaMalloc,c.byref(gpu_values),c.sizeof(values))
    try:
        check(runtime.cudaMemcpy,gpu_values,c.cast(values,c.c_void_p),c.sizeof(values),1)
        alpha=c.c_float(1.0);beta=c.c_float(0.0)
        blas.cublasSgemm_v2.argtypes=[c.c_void_p,c.c_int,c.c_int,c.c_int,c.c_int,c.c_int,
            c.POINTER(c.c_float),c.c_void_p,c.c_int,c.c_void_p,c.c_int,c.POINTER(c.c_float),c.c_void_p,c.c_int]
        check(blas.cublasSgemm_v2,handle,0,0,1,1,1,c.byref(alpha),gpu_values,1,
            c.c_void_p(gpu_values.value+4),1,c.byref(beta),c.c_void_p(gpu_values.value+8),1)
        check(runtime.cudaMemcpy,c.cast(values,c.c_void_p),gpu_values,c.sizeof(values),2)
        assert abs(values[2]-6.0)<1e-6,values[2]
        kernel_result={'operation':'1x1 SGEMM','input':[2.0,3.0],'expected':6.0,'actual':values[2],'passed':True}
    finally:check(runtime.cudaFree,gpu_values)
finally:check(blas.cublasDestroy_v2,handle)
selected_links={}
for name,path in [('cuda_runtime',cuda12[0]),('cublas',cublas_paths[0])]:
    result=subprocess.run(['ldd',str(path)],capture_output=True,text=True,check=True)
    assert 'not found' not in result.stdout,(path,result.stdout)
    selected_links[name]=result.stdout.strip()
packages=subprocess.run(['dpkg-query','-W','-f=${Package}\t${Version}\t${Status}\n'],capture_output=True,text=True,check=True)
installed={}
for line in packages.stdout.splitlines():
    fields=line.split('\t')
    if len(fields)==3 and fields[2]=='install ok installed':installed[fields[0]]=fields[1]
version_result=subprocess.run(['ollama','--version'],capture_output=True,text=True,timeout=15)
version_output=(version_result.stdout+'\n'+version_result.stderr).strip()
assert version_result.returncode==0 and re.search(r'(?<![0-9.])0\.40\.15(?![0-9.])',version_output),version_output
nvidia_smi=subprocess.run(['nvidia-smi','--query-gpu=name,driver_version','--format=csv,noheader'],capture_output=True,text=True,check=True)
print(json.dumps({'status':'passed','ollama_version':'0.40.15','ollama_version_output':version_output,
    'cuda_runtime_api_version':version.value,'cuda_runtime_library':str(cuda12[0]),'cuda_runtime_filename':cuda12[0].name,
    'cublas_api_version':blas_version.value,'cublas_library':str(cublas_paths[0]),
    'gpu_driver_observation':nvidia_smi.stdout.strip(),'gpu_device_count':count.value,'gpu_name':device_name.value.decode(),'compute_capability':str(major.value)+'.'+str(minor.value),
    'cuda_memory_round_trip':{'bytes':32,'value':90,'passed':True},'selected_library_dependencies':selected_links,
    'cublas_kernel_check':kernel_result,
    'library_inventory':libraries,'installed_os_packages':installed,
    'cudnn_files':[item for item in libraries if 'cudnn' in Path(item['path']).name],
    'selected_backend_scope':'CUDA 12.8 library and GPU readiness; Ollama automatic runner selection and inference remain untested.',
    'service_started':False,'model_downloaded':False,'inference_run':False},indent=2))
