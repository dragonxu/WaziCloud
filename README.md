![travis](https://travis-ci.org/Waziup/Platform.svg?branch=master)


WAZIUP platform
===============

The WAZIUP platform is an IoT Big Data platform.
It allows to create IoT applications and deploy them both in the Cloud and in the local gateway.

For information and documentation: http://www.waziup.io

Install
-------

Run:
```
git clone --recursive git@github.com:Waziup/Platform.git
cd Platform
mkdir -p data/mongo data/keycloak data/els
docker-compose build
docker-compose up
```

If elasticsearch complains about virtual memory, run this command and restart:
```
sudo sysctl -w vm.max_map_count=262144
```

You can then access Waziup platform on http://localhost

See [this file](INSTALL.md) for the installation instructions on Cloud platforms.


Debug
-----

To export the keycloak configuration, run:
```
docker-compose run --entrypoint "/opt/jboss/docker-entrypoint.sh -b 0.0.0.0 -Dkeycloak.migration.action=export -Dkeycloak.migration.provider=singleFile -Dkeycloak.migration.file=/opt/jboss/keycloak/standalone/data/waziup-realm.json" keycloak
```


Copyright
---------

Copyright 2016.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

