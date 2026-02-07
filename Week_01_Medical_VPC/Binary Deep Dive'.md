---
marp: true
theme: 2smogss
header: '🏥 VitalStream Medical: Binary Deep Dive'
footer: 'Robert Chich | Cloud Security Architect Journey'
paginate: true
---

# 🧬 Cracking the Binary Code
## Subnetting Beyond the Basics
**"When a /24 is too big and a /32 is too small."**

---

### 🚑 The Paramedic Perspective: MCI Logic

Think of this like a **Mass Casualty Incident (MCI)** where you have to divide a single treatment area into smaller, specialized zones on the fly. 

On the AWS SAA-C03 exam, you must "borrow" bits from the last octet to create these specialized zones.



---

### 🔢 The Binary "Zoom In": The 4th Octet

An IP address consists of 4 groups of 8 bits. Let’s look at the "hidden" binary table of the last group in your **10.50.1.0** subnet:

| Decimal Value | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Binary Bit** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

To create subnets smaller than a /24, we start locking these bits from **left to right**.

---

### 1️⃣ The /25 Breakdown: Splitting the Ward

If you change your subnet from a /24 to a /25, you are locking **one more bit** (the 128 bit).

- **Bits Locked:** 25
- **Bits Free:** 7 ($32 - 25 = 7$)
- **The Math:** $2^7 = 128$ total IP addresses.
- **Usable IPs:** $128 - 5 = \mathbf{123}$.

**The Result:** You just split your /24 street into two blocks:
* `10.50.1.0` to `10.50.1.127`
* `10.50.1.128` to `10.50.1.255`



---

### 2️⃣ The /26 Breakdown: The "Quarter" Split

If you lock **two bits** in that last octet (128 + 64), you are now at a /26.

- **Bits Locked:** 26
- **Bits Free:** 6 ($32 - 26 = 6$)
- **The Math:** $2^6 = 64$ total IP addresses.
- **Usable IPs:** $64 - 5 = \mathbf{59}$.

**Architectural Impact:** This allows for 4 distinct zones within a single traditional /24 range.

---

### 🎓 SAA-C03 "Exam Trap": VLSM Efficiency

The exam will test your ability to choose the most efficient CIDR block (Variable Length Subnet Mask).

**Scenario:** "You have 50 servers. Which block is the most efficient?"

| Candidate | CIDR | Total IPs | Usable IPs | Status |
| :--- | :---: | :---: | :---: | :--- |
| Candidate A | **/25** | 128 | 123 | Too much waste |
| **Candidate B** | **/26** | **64** | **59** | **THE WINNER** |
| Candidate C | **/27** | 32 | 27 | Not enough room |



---

### 🏥 Why this matters for VitalStream

In your current script, we used **/24** for everything because it’s easy to manage. 

However, if you were building a **Global Medical Network** with 500 small clinics, giving each a /24 (256 IPs) would exhaust your "Zip Codes" (IP space) instantly. 

**The Professional Solution:** Use a **/27** or **/28** for small satellite clinics to preserve your address space for the main hospital hubs.

---
