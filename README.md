# anomaly-detection

```
New-AzResourceGroup `
  -Name rg-adpoc `
  -Location westus2

New-AzResourceGroupDeployment `
  -ResourceGroupName rg-adpoc `
  -TemplateUri "azureDeploy.json"
```