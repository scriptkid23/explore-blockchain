#!/bin/bash

cd marketplace-frontend
git pull
npm run build
cd ..

ssh -i epicwars-backend.pem ubuntu@23.22.198.29 'rm -rf /var/www/epic/html/*'
scp -r -i epicwar.pem marketplace-frontend/dist ubuntu@23.22.198.29:/var/www/epic/html


