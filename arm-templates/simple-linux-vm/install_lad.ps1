param($resourceGroupName, $storageAccountName, $vmName, $eventHubNamespaceName, $eventHubName)

# Get the VM object
$vm = Get-AzVM -Name $vmName -ResourceGroupName $resourceGroupName

# Enable system-assigned identity on an existing VM
Update-AzVM -ResourceGroupName $resourceGroupName -VM $vm -IdentityType SystemAssigned

# Get the public settings template from GitHub and update the templated values for the storage account and resource ID
$publicSettings = (Invoke-WebRequest -Uri https://raw.githubusercontent.com/saptarshibasu/anomaly-detection/master/arm-templates/simple-linux-vm/lad_pub_settings.json).Content
$publicSettings = $publicSettings.Replace('__DIAGNOSTIC_STORAGE_ACCOUNT__', $storageAccountName)
$publicSettings = $publicSettings.Replace('__VM_RESOURCE_ID__', $vm.Id)

# If you have your own customized public settings, you can inline those rather than using the preceding template: $publicSettings = '{"ladCfg":  { ... },}'

# Generate a SAS token for the agent to use to authenticate with the storage account
$saSasToken = New-AzStorageAccountSASToken -Service Blob,Table -ResourceType Service,Container,Object -Permission "racwdlup" -Context (Get-AzStorageAccount -ResourceGroupName $resourceGroupName -AccountName $storageAccountName).Context -ExpiryTime $([System.DateTime]::Now.AddYears(10))

# $ehSasToken = (New-AzEventHubAuthorizationRuleSASToken -AuthorizationRuleId (New-AzEventHubAuthorizationRule -ResourceGroupName $resourceGroupName -Namespace $eventHubNamespaceName -EventHub $eventHubName -Name publishSasKey -Rights @("Send")).Id -KeyType Primary -ExpiryTime $([System.DateTime]::Now.AddYears(10))).SharedAccessSignature.Replace('Primary','publishSasKey').Trim()

# Build the protected settings (storage account SAS token)
$protectedSettings="{'storageAccountName': '$storageAccountName', 
                    'storageAccountSasToken': '$saSasToken',
                    'sinksConfig': {
                        'sink': [
                            {
                                'name': '$eventHubName',
                                'type': 'EventHub',
                                'sasURL': 'https://$($eventHubNamespaceName).servicebus.windows.net/$($eventHubName)?sr=$($eventHubNamespaceName).servicebus.windows.net%2f$($eventHubName)&sig=publishSasKey&skn=publishSasKey'
                            }
                        ]
                    }
                }"

# Finally, install the extension with the settings you built
Set-AzVMExtension -ResourceGroupName $resourceGroupName -VMName $vmName -Location $vm.Location -ExtensionType LinuxDiagnostic -Publisher Microsoft.Azure.Diagnostics -Name LinuxDiagnostic -SettingString $publicSettings -ProtectedSettingString $protectedSettings -TypeHandlerVersion 4.0
