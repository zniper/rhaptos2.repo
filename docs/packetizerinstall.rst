
New
================

1. remove nginx as it was installed as part of postboot
   sudo apt-get remove nginx-full

2. install apache, mysql, 
sudo apt-get install apache2 perl apache2-doc apache2-utils  libdbd-mysql-perl
sudo apt-get install mysql-server mysql-client 




3. Install Java
   sudo apt-get install openjdk-6-jre
   Install Java Crtypto
   http://www.oracle.com/technetwork/java/javase/downloads/jce-6-download-429243.html
  
   Install NetMesh 
   http://wso2.org/downloads/identity
   
   It uses OpenID4Java !
   sign in as admin/admin
   



OpenIDServer from packetizer

install mysql
-------------

sudo apt-get install mysql-server mysql-client
libdbd-mysql-perl
sudo apt-get install liburi-perl libcrypt-dh-perl libdigest-sha-perl libmath-bigint-perl libdata-random-perl 


Need CPAN to install Crypt::Random

sudo  perl -MCPAN -e shell 
install Crypt::Random
or

sudo  perl -MCPAN -e 'install Crypt::Random'


mysql -u root
mysql> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('yourpassword');

GRANT ALL PRIVILEGES ON *.* TO 'yourusername'@'localhost' IDENTIFIED BY 'yourpassword' WITH GRANT OPTION;

CREATE DATABASE oid;
mysql> show tables;
+---------------+
| Tables_in_oid |
+---------------+
| nonce         |
| openid_assoc  |
| openid_sigs   |
| openid_users  |
+---------------+
4 rows in set (0.00 sec)


Test Code::

   #!/usr/bin/perl                                                                        
   use strict;                                                                            
   use warnings;                                                                          
   use DBI;                                                                               

   my $username='pbrian';
   my $pass='qwerty1';                                                                
   my $db='mysql';  
   my $dbh = DBI->connect( "dbi:mysql:$db", $username, $pass, { 'PrintError' => 1, 'Raise Error' => 1 } );
   print $dbh;
   my $sql='select user, host from user';                                              
   my $sql_arg=1;                                                                         
   my $sql_handle=$dbh->prepare($sql);                                                    
   $sql_handle->execute();                                                        
   my @data;                                                                              
   while (@data=$sql_handle->fetchrow_array()) {                                          
       print join("\n",@data) 
	 }    


sudo mkdir -p /usr/local/lib/site_perl
put the library files in there
add a row to database
ensure the rewrite rules work ok, ensure templates in right position

   
