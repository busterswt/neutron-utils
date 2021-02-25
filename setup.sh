git clone https://github.com/busterswt/neutron-utils/ ~/neutron-utils

mkdir ~/venvs
python3 -m venv ~/venvs/neutron-utils
source ~/venvs/neutron-utils/bin/activate

python3 -m pip install -r requirements.txt
