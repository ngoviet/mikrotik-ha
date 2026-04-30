# Mikrotik Router — Home Assistant Integration

[![Add to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ngoviet&repository=mikrotik-ha&category=integration)
[![GitHub release](https://img.shields.io/github/v/release/ngoviet/mikrotik-ha?style=plastic)](https://github.com/ngoviet/mikrotik-ha/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=plastic)](LICENSE)

Giám sát và điều khiển thiết bị MikroTik RouterOS từ Home Assistant.

> Fork độc lập từ [tomaae/homeassistant-mikrotik_router](https://github.com/tomaae/homeassistant-mikrotik_router) — sửa lỗi, cập nhật HA 2026.x, tối ưu hiệu năng. Phát triển độc lập, không phụ thuộc upstream.

## Cài đặt

Click nút **Add to HACS** ở trên, hoặc thêm thủ công:

1. HACS → Integrations → ⋮ → **Custom repositories**
2. URL: `https://github.com/ngoviet/mikrotik-ha` — Category: **Integration**
3. Cài "Mikrotik Router" → **Restart HA**

## Yêu cầu

- **Home Assistant** ≥ 2024.3 (đã test 2026.4.4)
- **RouterOS** ≥ v6.43 / v7.1
- MikroTik user có quyền `api` + `read` (khuyến nghị: `write`, `reboot`, `policy`, `test`)

## Cấu hình MikroTik

```routeros
/user group add name=homeassistant policy=api,read,write,reboot,policy,test
/user add name=homeassistant group=homeassistant password=mật-khẩu
```

## Cấu hình Integration

**Settings → Devices & Services → Add Integration → Mikrotik Router**

| Trường | Giá trị |
|--------|---------|
| Name | Tên hiển thị |
| Host | IP MikroTik |
| Port | `0` (tự động: 8728 non-SSL / 8729 SSL) |
| Username / Password | User đã tạo ở trên |
| SSL | Bật nếu dùng port 8729 |

Sau khi thêm, ấn **Configure** để bật/tắt các nhóm sensor: Filter, NAT, Mangle, PPP, Kid Control, Device Tracker...

## Tính năng

| Nhóm | |
|------|--|
| Interface | Bật/tắt port, SFP, PoE, traffic RX/TX, theo dõi thiết bị kết nối |
| Firewall | Bật/tắt NAT, Mangle, Filter rules |
| QoS | Bật/tắt Simple Queues |
| Device Tracker | ARP, Wireless, CAPsMAN, Netwatch, DHCP leases |
| Kid Control | Theo dõi và tạm dừng thiết bị |
| Hệ thống | CPU, RAM, HDD, nhiệt độ, quạt, PSU, UPS, GPS |
| Firmware | Cập nhật RouterOS + RouterBOARD |
| Script | Chạy script MikroTik từ HA |
| Client Traffic | Accounting (v6) / Kid Control Devices (v7+) |
| Khác | PPP users, Captive Portal, 26 ngôn ngữ (có tiếng Việt) |

## Đã sửa so với upstream

- 7+ lỗi critical: crash, deadlock, race condition
- Tương thích HA 2024.3 → 2026.4.4
- Tương thích librouteros v3 + v4
- Tối ưu: bỏ API query không cần thiết

## License

Apache 2.0 — giữ nguyên từ upstream.
