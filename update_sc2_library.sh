# Clone develop branch from python-sc2
git clone -b develop https://github.com/BurnySc2/python-sc2 python-sc2

# Generate new requirements.txt
cd python-sc2
poetry export --format requirements.txt --output requirements.txt
cd ..

# Delete old sc2 subfolder, copy new requirements.txt and update sc2 subfolder
rm -rf sc2
mv python-sc2/requirements.txt requirements.txt
mv python-sc2/sc2 sc2/
rm -rf python-sc2
