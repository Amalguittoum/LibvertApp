#!/usr/bin/python
import libvirt
import sys
import os
quit=[]
verif =True
quit.append(False)
conn=libvirt.open("qemu:///system")
ls = conn.listAllDomains(0)


while not quit[0] :
   lsNact=conn.listDefinedDomains()
   lsAct=conn.listDomainsID()
   print "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n"
   print "=-=-=-=-=-=-=-=-TP   Libvert__Management des Machines virtuelles-=-=-=-=-=-=-=-=\n"
   print "         0) Information sur la machine hyperviseur.\n"
   print "         1) Lister les machines virtuelles.\n"
   print "         2) demarrer une machine.\n"
   print "         3) Arreter une machine .\n"
   print "         4) L adresse IP d une machine virtuelle donnee\n"
   print "         5) Quitter.\n"
   print "               Votre choix : "
   num=input()
   while verif :
      if num >= 6 : 
         print "Erreur !! Veuillez entrer un nemero de choix correcte !! \n"
         num=input()
      else : verif=False
  
#**************************************************************# 

#**************************************************************# 
   def NomHyperv():
      host = conn.getHostname()
      print('Hostname:'+host)
      #Max virtual CPU
      vcpus = conn.getMaxVcpus(None)
      print('Maximum support virtual CPUs: '+str(vcpus))
      #Host Infos
      info = conn.getInfo()
      print('Model: '+str(info[0]))
      print('Memory size: '+str(info[1])+'MB')
      print('Number of CPUs: '+str(info[2]))
      print('MHz of CPUs: '+str(info[3]))
      print('Number of NUMA nodes: '+str(info[4]))
      print('Number of CPU sockets: '+str(info[5]))
      print('Number of CPU cores per socket: '+str(info[6]))
      print('Number of CPU threads per core: '+str(info[7]))
      #Virtualization type
      print('Virtualization type: '+conn.getType())
      raw_input("Appuyer sur une touche pour revenir")
       
#**************************************************************#
   def ListerVm():
      print "Les machines virtuelles existantes: .\n"
      j=0
      for vm in ls :
         print "      " +str(j)+") " + vm.name() +"\n"
         j=j+1
      raw_input("Appuyer sur une touche pour revenir")
#**************************************************************#




#**************************************************************#
   def DemareVm():
      i=0
      check=True
      for vm in lsNact:
         print str(i) +") "+vm 
         i=i+1
      if len(lsNact)==0 : print "Aucune machine a demarrer !"
      else :
         print "Veuillez choisir la machine :\n"
         num=input()  
         while check :
           if num >= len(lsNact) : 
              print "Erreur !! Veuillez entrer le numero de la machine \n"
              num=input()
           else : check=False
         print lsNact[num] +" entrain de demarer ..."
         vm=conn.lookupByName(lsNact[num])
         vm.create()
         #os.system("virt-viewer "+vm.name()+" &")
	 os.system("gnome-terminal -x virt-viewer "+vm.name()+" &")
      raw_input("Appuyer sur une touche pour revenir")
       
#**************************************************************#
   def ArretVm():
     
      i=0
      check=True
      for id in lsAct:
         dom=conn.lookupByID(id)
         print str(i) +") "+dom.name()
         i=i+1
      if len(lsAct)==0 : print "Aucune machine est allumee!!"
      else :
         print "Veuillez choisir la machine :\n"
         num=input()  
          
         while check :
            if num >= len(lsAct) : 
               print "Erreur !! Veuillez entrer le numero de la machine \n"
               num=input()
            else : check=False
         dom=conn.lookupByID(lsAct[num])
         print dom.name() +" entrain de s'arreter ..."
         dom.destroy()
      raw_input("Appuyer sur une touche pour revenir")
#**************************************************************#
   def IPVm():
      i=0
      check=True
      for id in lsAct:
         dom=conn.lookupByID(id)
         print str(i) +") "+dom.name()
         i=i+1
      if len(lsAct)==0 :print "Aucune machine est allumee !! \n vous ne pouvez pas connaitre l'adresse IP des machines eteintes !!\n"
      else :
         print "Veuillez choisir la machine :\n"
         num=input()
         while check :
            if num >= len(lsAct) : 
               print "Erreur !! Veuillez entrer le numero de la machine \n"
               num=input()
            else : check=False
              
         def getIP(domainName):
            dom = conn.lookupByName(domainName)
            if dom == None:
               print 'Failed to get the domain object'
            ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
            print "The interface IP addresses:"
            for (name, val) in ifaces.iteritems():
               print "l'interface  :"+name
               if val['addrs']:
                  for ipaddr in val['addrs']:
                     if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                        print " IPV4_address : "+ipaddr['addr']
                     elif ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV6:
                        print " IPV6_address : " +ipaddr['addr']
 
      
         dom=conn.lookupByID(lsAct[num])
         getIP(dom.name())
      raw_input("Appuyer sur une touche pour revenir")
#**************************************************************#
   def quitter():
      print "Vous voulez quitter oui/non "
      rep=raw_input()
      
      if rep=="oui": 
         quit[0]=True
         conn.close()
 
#**************************************************************#
   options = {
                0 : NomHyperv,
                1 : ListerVm,
                2 : DemareVm,
                3 : ArretVm,
                4 : IPVm,
                5 : quitter
               
   }
   options[int(num)]()
