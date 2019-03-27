# Ubuntu+tools, python, pip, python modules
#apt-get update
#apt-get install -y wget g++ libtool rsync make x11-apps python3-dev python3-numpy python3-pip python3-tk 
#rm -rf /var/lib/apt/lists/*
#pip install --no-cache-dir matplotlib scipy numpy scikit-learn keras tensorflow jupyter metakernel zmq notebook==5.* plaidml-keras plaidbench energyflow

apt-get update 
apt-get install -y cmake
wget http://xrootd.org/download/v4.9.0/xrootd-4.9.0.tar.gz && \
    tar zxf xrootd-4.9.0.tar.gz && \
    mkdir build-xrootd && \
    cd build-xrootd && \
    cmake ../xrootd-4.9.0 && \
    make && make install && \
    cd .. && rm -rf build-xrootd
pip install --no-cache-dir matplotlib scipy numpy scikit-learn keras tensorflow jupyter metakernel zmq notebook==5.* plaidml-keras plaidbench energyflow uproot
