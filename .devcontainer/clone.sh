mkdir /src
chown -R vscode /src
cd /src
su vscode -c "git clone --depth 1 https://github.com/Azure/azure-cli --branch dev"

