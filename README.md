# What is this?

This is part of diploma project to prove that routine aspects of WorldSkills Russia Skill #39 expert's work can be automated.

### How this works?
Python3 script do this sequence of actions:

1. Access host's port with telnet
2. Login to COM-over-Telnet
3. Send script that checks competitive task compliance.
4. Run it and return 64 bit number that can be used to generate report.

Firstly if you are using VMWare vSphere don't forget to open ports in firewall

### How to make this work on Linux?

You will need to edit your bootloader settings. I used this as example https://www.cyberciti.biz/faq/howto-setup-serial-console-on-debian-linux/

### So this works on Linux how about Windows?
For windows serial management you should enable __[EMS](https://en.wikipedia.org/wiki/Emergency_Management_Services)__ 
```
bcdedit /emssettings EMSPORT:1 EMSBAUDRATE:115200
bcdedit /ems {default} ON
bcdedit /bootems {default} ON
bcdedit /ems ON
bcdedit /bootems ON
```

### Network devices?

If you are using virtual network equipment like GNS3 you should be fine. For real devices this can be complicated cause you will need to use either NM-16/32A cisco module, PCI(-E) Card with DB62 or special serial terminal server.

### Text User Interface

Text user interface i used by default you can navigate hosts by left and right arrows and machines in that host by up and down arrows.

Pressing Enter or Space button will cause machine to be canceled or restarted. You can use that to edit and reload check script on fly.

Press q to exit and wait until report generation.

### Reports

Reports are just CSV files that decoded from 64 bit number result if there is ```-``` symbol in start that means that script failed to check that machine. 

In the end you can make Excel file that will accept csv results and make a proper spreadsheet.
