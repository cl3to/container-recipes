"""
OMPC-NEXTGEN-DEV 0.0.1
This Image is used for development of OpenMP Cluster (OMPC) nextgen plugin on LLVM/OpenMP/Libomptarget.

Contents:
  Ubuntu 22.04
  CMAKE 3.29.0
  LLVM 17 (Clang, LLD, LLDB, libc++, libc++abi, compiler-rt)
  UCX 1.15.0
  MPICH 4.2.0
  TOOLS (git, ccache, wget, ninja-build, gdb)
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
    apt=[
        'autoconf',
        'automake',
        'build-essential',
        'ca-certificates',
        'ccache',
        'gdb',
        'gfortran',
        'git',
        'gnupg',
        'gzip',
        'hwloc',
        'libelf-dev',
        'libfabric-dev',
        'libglib2.0-dev',
        'libgraphviz-dev',
        'libhwloc-dev',
        'libnuma-dev',
        'libssl-dev',
        'ninja-build',
        'openssh-client',
        'pdsh',
        'pkg-config',
        'wget',
    ],
)

# Python
python = python(python2=False, devel=True)
Stage0 += python

Stage0 += packages(
    apt=[
        'python3-distutils',
        'python3-psutil',
    ]
)

# CMAKE
Stage0 += cmake(eula=True, version='3.29.0')

# LLVM
llvm = llvm(
    upstream=True,
    version='17',
    openmp=False,
    toolset=True,
)
Stage0 += llvm
Stage0 += llvm.runtime()

Stage0 += environment(
    variables={
        'CC': '/usr/bin/clang',
        'CXX': '/usr/bin/clang++',
        'LIBRARY_PATH': '/usr/lib/x86_64-linux-gnu/:/usr/local/lib:$LIBRARY_PATH',
        'LD_LIBRARY_PATH': '/usr/lib/x86_64-linux-gnu/:/usr/local/lib:$LD_LIBRARY_PATH',
    }
)

# KNEM and XPMEM
Stage0 += knem(ldconfig=True)
Stage0 += xpmem(ldconfig=True)

# OFED
Stage0 += mlnx_ofed(ldconfig=True)

# UCX
ucx = ucx(
    version='1.15.0',
    toolchain=llvm.toolchain,
    cuda=False,
    knem="/usr/local/knem",
    ldconfig=True,
    ofed=True,
    xpmem="/usr/local/xpmem",
)
Stage0 += ucx

# MPICH
mpich = mpich(
    version='4.2.0',
    toolchain=llvm.toolchain,
    with_ucx='/usr/local/ucx',
    without_cuda=True,
    with_hwloc=True,
    with_hydra=True,
    with_pci=True,
    with_device='ch4',
)
Stage0 += mpich

Stage0 += comment('Set the environment variables.')
Stage0 += environment(
    variables={
        'CPATH': '/usr/local/mpich/include:$CPATH',
    }
)
