# IGW vs NAT gw

for reaching the internet:
there must be a route to IGW. eg
- -> TGW -> IGW
- NAT gw -> IGW

Public subnet means theres a route table with route to IGW.
so hosts in public subnet are internet addressable. 

NAT gw is for private subnet (hosts with private ip) to connect to the internet (only OUTBOUND traffic - instances are not internet addressable).
NAT gw sits in public subnet since it needs to be publicly addressable to recv responses from internet. 
If private subnet has route table with route to NAT gw then instances with private ip can reach the internet.

IGW is a proxy for public subnet (instances with public ip). Instances in public subnet are internet addressable.

### Qns
1. Why does NAT gateway have to be in public subnet? I think on cloud network is implemented by virtual nodes. So why couldn't it be for NAT gateway to act like router in a private subnet, to do NAT when destination address is outside the private network it is also part of?

2. Why does NAT gateway still require traffic of public subnet it has to be part of to be routed to internet gateway by a route table of same subnet? I mean, NAT gateway should be sufficient in itself to get that traffic gone to internet by being part of some public subnet already. Why does this IGW association with NAT gateway have to be done manually?

An Internet Gateway is a logical connection between a VPC and the Internet. If there is no Internet Gateway, then the VPC has no direct access to the Internet. (However, Internet access might be provided via a Transit Gateway, which itself would need an Internet Gateway.)

Think of the Internet Gateway as the wire that you use to connect your home router to the Internet. Pull out that wire and your home network won't be connected to the Internet.

A subnet is a 'public subnet' if it has a Route Table that references an Internet Gateway.

A NAT Gateway receives traffic from a VPC, forwards it to the Internet and then returns the response that was received. It must live in a public subnet because it needs to communicate with the Internet (and therefore needs a route to the Internet Gateway).

Resources in a private subnet (which, by definition, cannot route to the Internet Gateway) will have their Internet-bound requests sent to the NAT Gateway (due to a Route Table configuration). The NAT Gateway will then forward that request to the Internet and return the response that was received from the Internet.

NAT Gateways exist because organizations want the additional security offered by private subnets, which guarantee that there is no inbound access from the Internet. Similar security can be provided with a Security Group, so private subnets aren't actually required. However, people who are familiar with traditional (non-cloud) networking are familiar with the concept of public and private subnets, so they want to replicate that architecture in the cloud. Physical network routers only apply rules at the boundary of subnets, whereas Security Groups can be applied individually to each Resource. It's a bit like giving each resource its own router.

A NAT Gateway is not very complex. In fact, you can run a NAT instance on Amazon EC2 that does a similar job. Simply launch an Amazon EC2 instance and run this script:

sudo sysctl -w net.ipv4.ip_forward=1
sudo /sbin/iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo yum install iptables-services
sudo service iptables save
A NAT Gateway is a bit more sophisticated in that it automatically scales based on the traffic being served and will automatically redeploy any failed infrastructure. It is, effectively, a "managed, auto-scaled NAT instance".

You are right that all of the above is implemented as a virtual network. There is no physical device called an Internet Gateway or a NAT Gateway. Much of it is logical routing, although the NAT Gateway does involve launching infrastructure behind-the-scenes (probably on the same infrastructure that runs EC2 instances). The NAT Gateway only connects to one VPC -- it is not a 'shared service' like Amazon S3, which is available to many AWS users simultaneously.

