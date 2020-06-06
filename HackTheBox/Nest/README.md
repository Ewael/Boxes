# Nest

Author: Ewaël

**Nest** is an easy HackTheBox box by VbScrub.

`nmap -sC -sV -oN nmap 10.10.10.178 -v -A` shows only port 445 is open. Let's see if I can see some files anonymously.

```
$ smbclient -L //10.10.10.178

Enter WORKGROUP\root's password:

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	Data            Disk
	IPC$            IPC       Remote IPC
	Secure$         Disk
	Users           Disk
SMB1 disabled -- no workgroup available
```

I can't access `ADMIN$` and `C$`. `Users` contains directories that I can't list but `Data` has some interesting files. I find `Welcome Email.txt` in `\Shared\Templates\HR` that I transfer on host using `get [file]` but `mget *` works too.

```
Username: TempUser
Password: welcome2019
```

I can now log as `TempUser` in `Users` with `smbclient //10.10.10.178/Users -U TempUser` but there's nothing interesting in my directory. Going back to `Data` I see that I can now access `Configs`. I find

```xml
  <Username>c.smith</Username>
  <Password>fTEzAfYDoz1YzkqhQkH6GQFYKp1XY5hm7bjOP86yYxE=</Password>
```

in `RU_config.xml` but I can't decrypt the password yet. In *Notepad++* config file I find a nice path: `\\HTB-NEST\Secure$\IT\Carl\Temp.txt` that I can go to even if `IT` is not listable as `TempUser`. Once in `Carl` directory I start checking every files and I finally get something interesting in `\IT\Carl\VB Projects\WIP\RU\RUScanner\Utils.vb`:

```VB.NET
...
Return Decrypt(EncryptedString, "N3st22", "88552299", 2, "464R5DFA5DL6LE28", 256)
...
```

I search for `N3st22` encryption and I find a site with this exact function [https://dotnetfiddle.net/bjoBP6](https://dotnetfiddle.net/bjoBP6) that I modify with the password found earlier:

```VB.NET
...
Console.WriteLine("Decrypted: " + DecryptString("fTEzAfYDoz1YzkqhQkH6GQFYKp1XY5hm7bjOP86yYxE="))
...
```

It returns me `C.Smith`'s password `xRxRxPANCAK3SxRxRx` that I use to get my user flag in `Users`:

`cf71b25404be5d84fd827e05f426e987`

Moving around in `C.Smith` dir I find an executable in `\C.Smith\HQK Reporting\AD Integration Module` named `HqkLdap.exe`. After trying some reverse in Ghidra I decide to execute it on Windows and to reverse it using dotPeek. Running it does not work because a config file is missing but reversing it shows me a new encrypting function:

```VB.NET
...
return string.IsNullOrEmpty(EncryptedString) ? string.Empty : CR.RD(EncryptedString, "667912", "1313Rf99", 3, "1L1SA61493DRV53Z", 256);
...
```

I find it there too [https://dotnetfiddle.net/1ca3i6](https://dotnetfiddle.net/1ca3i6) and I start searching for the encrypted password. Fun fact: the encrypted password is already the one on the site and so is the admin password but I don't know it yet.

After loosing some time trying to get an encrypted password in the binary, I decide to check if I did not miss anything in the `C.Smith` directory. I find this `Debug Mode Password.txt` file in `\C.Smith\HQK Reporting` but it's empty, which is annoying because it really looks like what I'm searching for.

Some googling later I finally find `allinfo` command which shows me the other streams on a NTFS partition.

```
\C.Smith\HQK Reporting\> allinfo "Debug Mode Password.txt"
altname: DEBUGM~1.TXT
create_time:    Thu Aug  8 07:06:12 PM 2019 EDT
access_time:    Thu Aug  8 07:06:12 PM 2019 EDT
write_time:     Thu Aug  8 07:08:17 PM 2019 EDT
change_time:    Thu Aug  8 07:08:17 PM 2019 EDT
attributes: A (20)
stream: [::$DATA], 0 bytes
stream: [:Password:$DATA], 15 bytes
```

I use `get "Debug Mode Password.txt":password` to transfer the right one and I have now the password for the debug mode. I have no idea what it means so I start searching where this password could be useful. In the `HKQ Reporting` configuration file there is a mention of the 4386 port. `nc 10.10.10.178 4386` does not seem to work but `telnet 10.10.10.178 4386` does.

```
>help

This service allows users to run queries against databases using the legacy HQK format

--- AVAILABLE COMMANDS ---

LIST
SETDIR <Directory_Name>
RUNQUERY <Query_ID>
DEBUG <Password>
HELP <Command>
```

Let's use the password I just got.

```
>DEBUG WBQ201953D8w

Debug mode enabled. Use the HELP command to view additional commands that are now available
>HELP

This service allows users to run queries against databases using the legacy HQK format

--- AVAILABLE COMMANDS ---

LIST
SETDIR <Directory_Name>
RUNQUERY <Query_ID>
DEBUG <Password>
HELP <Command>
SERVICE
SESSION
SHOWQUERY <Query_ID>
```

I use `setdir ..` then `list` to list the files. In `LDAP` dir I find the `Ldap.conf` that I print with `showquery`:

```
Domain=nest.local
Port=389
BaseOu=OU=WBQ Users,OU=Production,DC=nest,DC=local
User=Administrator
Password=yyEq0Uvvhq2uQOcWG8peLoeRQehqip/fKdeG/kjEVb4=
```

That's the password I was searching for. I decrypt it with the online function I found in the binary and I get the decrypted password: `XtH4nkS4Pl4y1nGX`

In `Users` there is a link to `c$` in the `Administrator` dir, and I find the root password in `c$` with the decrypted password:

`6594c2eb084bc0f08a42f0b94b878c41`
