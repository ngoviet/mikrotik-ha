# Mikrotik Router — Home Assistant Integration

[![Add to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ngoviet&repository=mikrotik-ha&category=integration)
![GitHub release](https://img.shields.io/github/v/release/ngoviet/mikrotik-ha?style=plastic)
![Project Stage](https://img.shields.io/badge/project%20stage-Production%20Ready-green.svg?style=plastic)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=plastic)

> Fork độc lập từ [tomaae/homeassistant-mikrotik_router](https://github.com/tomaae/homeassistant-mikrotik_router) — sửa lỗi, cập nhật HA 2026.x, tối ưu hiệu năng.

---

## Cài đặt

**Cách 1 — Click nút trên:**  
[![Add to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ngoviet&repository=mikrotik-ha&category=integration)

**Cách 2 — Thêm thủ công:**
1. HACS → Integrations → ⋮ → **Custom repositories**
2. URL: `https://github.com/ngoviet/mikrotik-ha` — Category: **Integration**
3. Cài "Mikrotik Router" → **Restart HA**

## Yêu cầu

- Home Assistant ≥ 2024.3 (đã test **2026.4.4**)
- RouterOS ≥ v6.43 / v7.1
- MikroTik user có quyền `api` + `read` (nên thêm `write`, `reboot`, `policy`, `test`)

## Tính năng

| Nhóm | Chi tiết |
|------|----------|
| **Interface** | Bật/tắt port, SFP, PoE, traffic RX/TX, theo dõi thiết bị kết nối |
| **Firewall** | Bật/tắt NAT, Mangle, Filter rules |
| **QoS** | Bật/tắt Simple Queues |
| **Device Tracker** | ARP, Wireless, CAPsMAN, Netwatch, DHCP leases |
| **Kid Control** | Theo dõi + tạm dừng thiết bị |
| **Hệ thống** | CPU, RAM, HDD, nhiệt độ, quạt, PSU, UPS, GPS |
| **Firmware** | Cập nhật RouterOS + RouterBOARD |
| **Script** | Chạy script MikroTik từ HA |
| **Traffic** | Accounting (v6) / Kid Control Devices (v7+) |
| **Khác** | PPP users, Captive Portal, 26 ngôn ngữ (có tiếng Việt) |

## Cấu hình MikroTik

```routeros
/user group add name=homeassistant policy=api,read,write,reboot,policy,test
/user add name=homeassistant group=homeassistant password=mật-khẩu
```

## Cấu hình Integration

Vào **Settings → Devices & Services → Add Integration → Mikrotik Router**

| Trường | Điền |
|--------|------|
| Name | Tên hiển thị |
| Host | IP MikroTik |
| Port | `0` (tự chọn 8728/8729) |
| Username / Password | User đã tạo |
| SSL | Bật nếu dùng port 8729 |

Sau khi thêm, ấn **Configure** để bật/tắt từng nhóm sensor: Filter, NAT, Mangle, PPP, Kid Control, Device Tracker...

## Khác biệt với upstream

- **7+ lỗi critical** đã sửa (crash, deadlock, race condition)
- Tương thích **HA 2024.3 → 2026.4.4**
- Tương thích **librouteros v3 + v4**
- Tối ưu: skip API query khi tính năng không dùng
- Phát triển độc lập, không phụ thuộc upstream

## License

Apache 2.0
