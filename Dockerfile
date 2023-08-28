# Pull a base image
 FROM ubuntu:20.04

# Copy everything (minus anything specified in .dockerignore) into the image
COPY . /opt/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes

# To make installs not ask questions about timezones
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York

##############################
# install base dependencies
# - for R repository
#   - dirmngr
#   - gpg-agent
# - for bookdown compilation
#   - pandoc, pandoc-citeproc, texlive-base, texlive-latex-extra
##############################

RUN \
  apt-get update \
    && \
  apt-get install -y -qq --no-install-recommends \
    software-properties-common \
    curl \
    g++-10 \
    make\
    cmake \
    python3=3.8.2-0ubuntu2 \
    python3-pip \
    python3-virtualenv \
    git=1:2.25.1-1ubuntu3 \
    dirmngr \
    gpg-agent \
    pandoc \
    pandoc-citeproc \
    texlive-base \
    texlive-latex-extra \
    lmodern \
    && \
  echo "installed base dependencies"

########################################################
# install r with whatever r packages we need/want
# - source: https://rtask.thinkr.fr/installation-of-r-4-0-on-ubuntu-20-04-lts-and-tips-for-spatial-packages/
########################################################
RUN \
  gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 \
    && \
  gpg -a --export E298A3A825C0D65DFD57CBB651716619E084DAB9 | apt-key add - \
    && \
  apt update \
    && \
  add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/' \
    && \
  apt-get install -y -q --no-install-recommends \
    r-base \
    r-base-dev \
    libssl-dev \
    libcurl4-openssl-dev \
    libfreetype6-dev \
    libmagick++-dev \
    libxml2-dev \
    libfontconfig1-dev \
    cargo \
    && \
  R -e "install.packages('rmarkdown', dependencies=NA, repos='http://cran.rstudio.com/')" \
    && \
  R -e "install.packages('knitr', dependencies=NA, repos='http://cran.rstudio.com/')" \
    && \
  R -e "install.packages('bookdown', dependencies=NA, repos='http://cran.rstudio.com/')" \
    && \
  R -e "install.packages('tidyverse', dependencies=NA, repos='http://cran.rstudio.com/')" \
    && \
  R -e "install.packages('cowplot', dependencies=NA, repos='http://cran.rstudio.com/')" \
    && \
  R -e "install.packages('plyr', dependencies=NA, repos='http://cran.rstudio.com/')" \
    && \
  R -e "install.packages('Hmisc', dependencies=NA, repos='http://cran.rstudio.com/')" \
    && \
  R -e "install.packages('ggplot2', dependencies=NA, repos='http://cran.rstudio.com/')" \
    && \
  R -e "install.packages('dplyr', dependencies=NA, repos='http://cran.rstudio.com/')" \
    && \
  R -e "install.packages('PupillometryR', dependencies=NA, repos='http://cran.rstudio.com/')" \
    && \
  echo "installed r and configured r environment"

########################################################
# install osfclient, use to download project data
########################################################
RUN \
  pip3 install osfclient \
    && \
  export OSF_PROJECT=qz3g7 \
    && \
  export PROJECT_PATH=/opt/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/DATA/ \
    && \
  mkdir PROJECT_PATH \
    && \
  osf -p ${OSF_PROJECT} fetch diagnostics-data.tar.gz ${PROJECT_PATH}diagnostics-data.tar.gz \
    && \
  tar -xzvf ${PROJECT_PATH}diagnostics-data.tar.gz -C ${PROJECT_PATH} \
    && \
  echo "download"

########################################################
# build supplemental material (will also run data analyses)
########################################################
RUN \
  cd /opt/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/ \
    && \
  ls -l \
    && \
  cd /opt/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/Experiments/Base_Diagnostics/Bookdown \
    && \
  chmod +x build_book.sh \
    && \
  ./build_book.sh \
    && \
  echo "compiled bookdown base diagnostic ebook" \
    && \
  cd /opt/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/Experiments/MVC_Diagnostics/Bookdown \
    && \
  chmod +x build_book.sh \
    && \
  ./build_book.sh \
    && \
  echo "compiled bookdown mvc diagnostic ebook" \
    && \
  cd /opt/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/Experiments/Base_Scheme_Parameter_Sweep/Bookdown \
    && \
  chmod +x build_book.sh \
    && \
  ./build_book.sh \
    && \
  echo "compiled bookdown selection scheme sweep ebook" \
    && \
  cd /opt/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/Experiments/MVC_Scheme_Parameter_Sweep/Bookdown \
    && \
  chmod +x build_book.sh \
    && \
  ./build_book.sh \
    && \
  echo "compiled bookdown selection scheme sweep mvc ebook" \
    && \
  cd /opt/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/Experiments/Nondominated_Sorting_Contradictory_Objectives/Bookdown \
    && \
  chmod +x build_book.sh \
    && \
  ./build_book.sh \
    && \
  echo "compiled bookdown nondominated sorting parts on contradictory objectives ebook" \
    && \
  cd /opt/ECJ-2023-Suite-Of-Diagnostic-Metrics-For-Characterizing-Selection-Schemes/ \
    && \
  ls -Rl Books/ \