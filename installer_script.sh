set -o errexit

#Chrome
STORAGE_DIR=/opt/render/project/.render

if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Downloading Chrome"
  echo $HOME
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm ./google-chrome-stable_current_amd64.deb
  cd $HOME # Make sure we return to where we were
else
  echo "...Using Chrome from cache"
fi
export PATH="/opt/render/project/.render/chrome/opt/google/chrome:$PATH"

#requirements
pip install -r requirements.txt