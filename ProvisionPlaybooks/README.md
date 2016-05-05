# Provision playbooks

### What it does
* Create root folders to hold campaign defintion/content, playbooks and audience rules
* Create 3 audience template and associate to file structure
    * Customers who purchased a product in a category
    * Customers who abandoned their cart
    * First Order Anniversary
* Create 2 campaign playbooks and associte to file structure
    * Abandoned Cart
    * Purchased in Category

### Configration
Change the config by open data.json, where you could update:
* docker host ip
* target tenant
* user/passwd to access polaris


### To run the script
```sh
python playbook.py 
```