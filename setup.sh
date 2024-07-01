#!/bin/bash

# Download wkhtmltopdf
wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.deb

# Install the package
sudo apt-get install -y ./wkhtmltox_0.12.6-1.bionic_amd64.deb

# Cleanup
rm wkhtmltox_0.12.6-1.bionic_amd64.deb
