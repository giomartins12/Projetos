'''
- Subir uma instância Linux no AWS EC2
'''

import boto3

name_inst = input(" Digite o nome da Instância: ")

nome_instancia = f"{name_inst}"
subnet_id = "nome_da_sub_rede"
group_seg_id = "nome_do_grupo_segurança"
ec2 = boto3.client('ec2', 'us-east-1',
                   aws_access_key_id='Key_id',
                   aws_secret_access_key='secret_key')

pem_file = open("{}.pem".format(nome_instancia),"w")
pem_file.write("")
print("Criando chave privada!")
chave = ec2.create_key_pair(KeyName=nome_instancia)
print("{}".format(chave))
pem_file.write(chave['KeyMaterial'])
pem_file.close()

execute_ec2 = ec2.run_instances(
                         InstanceType="t2.micro",
                         MaxCount=1,
                         MinCount=1,
                         ImageId="ami-0c4f7023847b90238",
                         #keyName=keySSH,
                         TagSpecifications=[
                             {'ResourceType': 'instance',
                              'Tags': [{'Key': 'Name', 'Value': nome_instancia}]
                              }], NetworkInterfaces=[{"SubnetId": subnet_id, 'AssociatePublicIpAddress': True,
                                            'DeviceIndex': 0, 'Groups': [group_seg_id]}])

print(">>>> criando instância(s)")
print("{}".format(execute_ec2))
print("Estância criada!")
estancias = ec2.describe_instances()
print(estancias)