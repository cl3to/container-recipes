"""
OMPC-DEV 0.0.1
This Image is used for development of OpenMP Cluster (OMPC) plugin on LLVM.

Contents:
  Ubuntu 22.04
  CMAKE 3.29.0
  LLVM 18 (Clang, LLD, LLDB, libc++, libc++abi, compiler-rt)
  MPICH 4.2.0
  TOOLS (git, ccache, wget, ninja-build)
"""
# pylint: disable=invalid-name, undefined-variable, used-before-assignment
# pylama: ignore=E0602

# add docstring to Dockerfile
Stage0 += comment(__doc__.strip(), reformat=False)

# Image recipe
Stage0 += comment('Set the ubuntu version to 22.04.')
Stage0 += baseimage(image='ubuntu:22.04')

Stage0 += comment('Install the required packages.')

# Tools

Stage0 += packages(
    ospackages=[
        'gzip',
        'wget',
        'git',
        'ninja-build',
        'autoconf',
        'automake',
        'ccache'
    ],
)

# CMAKE
Stage0 += cmake(eula=True, version='3.29.0')

# LLVM
llvm = llvm(
    upstream=True,
    version='18',
    openmp=False,
    toolset=True,
)
Stage0 += llvm

Stage0 += environment(
    variables={'CC': '/usr/bin/clang', 'CXX': '/usr/bin/clang++'}
)

# KNEM and XPMEM
# Stage0 += knem(ldconfig=True)
# Stage0 += xpmem(ldconfig=True)

# OFED
# Stage0 += mlnx_ofed()

# UCX
# Stage0 += ucx(
#     version='1.13.1',
#     toolchain=llvm.toolchain,
#     cuda=False,
#     # with_verbs="/usr",
#     # with_rdmacm="/usr",
#     # knem="/usr/local/knem",
#     # ldconfig=True,
#     # ofed=True,
#     # xpmem="/usr/local/xpmem",
#     # disable_static=True,
#     # enable_mt=True
# )


# MPICH
mpich = mpich(
    version='4.2.0',
    toolchain=llvm.toolchain,
    # with_ucx='/usr/local/ucx',
    without_cuda=True,
    without_ucx=True,
    without_verbs=True,
    with_hwloc=True,
    with_hydra=True,
    with_pci=True,
    with_device='ch4',
    disable_fortran=True,
    ospackages=['libnuma-dev', 'hwloc', 'libhwloc-dev', 'libfabric-dev'],
)
Stage0 += mpich

Stage0 += comment('Set the environment variables.')
Stage0 += environment(
    variables={
        'PATH': 'usr/local/bin:$PATH',
        'LD_LIBRARY_PATH': '/usr/local/lib:$LD_LIBRARY_PATH',
        'LIBRARY_PATH': '/usr/local/lib:$LIBRARY_PATH',
        'CPATH': '/usr/local/mpich/include:$CPATH',
    }
)
