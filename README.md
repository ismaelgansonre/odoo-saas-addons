# Odoo SaaS Addons
✅ 4️⃣ Recharge ton module à chaque changement

Si tu modifies le code d’un module, relance :


`
docker exec -it odoo_saas_web bash
odoo -d template_inventory_db -u inventory_saas`


💡 Cela met à jour ton module sans le désinstaller.

⚠️ Si ton module n’apparaît toujours pas :

Voici les points à vérifier :

Ton module contient bien un fichier __manifest__.py

Ton addons_path pointe bien sur le bon dossier

Ton docker-compose.yml monte bien le volume :

- ../odoo-saas-addons:/mnt/odoo-saas-addons


Tu as bien redémarré Odoo :

docker compose restart web