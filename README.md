# Mikrotik Router — Home Assistant Integration

[![Add to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ngoviet&repository=mikrotik-ha&category=integration)
![GitHub release](https://img.shields.io/github/v/release/ngoviet/mikrotik-ha?style=plastic)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=plastic)](https://github.com/hacs/integration)
![Project Stage](https://img.shields.io/badge/project%20stage-Production%20Ready-green.svg?style=plastic)

> **Fork** từ [tomaae/homeassistant-mikrotik_router](https://github.com/tomaae/homeassistant-mikrotik_router), phát triển độc lập với các bản sửa lỗi, cập nhật tương thích HA mới nhất, và tối ưu hiệu năng.

## Cài đặt nhanh

[![Add to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ngoviet&repository=mikrotik-ha&category=integration)

Hoặc thêm thủ công trong HACS:
1. HACS → Integrations → ⋮ (menu) → **Custom repositories**
2. Repository: `https://github.com/ngoviet/mikrotik-ha`
3. Category: **Integration**
4. Cài đặt "Mikrotik Router" và **restart HA**

## Yêu cầu

- **Home Assistant** 2024.3+ (đã test với 2026.4.4)
- **RouterOS** v6.43+ / v7.1+
- **librouteros** ≥3.4.1

## Tính năng

### Quản lý Interface
- Bật/tắt interface, xem trạng thái SFP, PoE
- Giám sát traffic RX/TX từng interface
- Theo dõi thiết bị kết nối (IP, MAC, Link)

### Firewall & QoS
- Bật/tắt **NAT**, **Mangle**, **Filter** rules
- Bật/tắt **Simple Queues**
- **Kid Control**: theo dõi và tạm dừng

### Theo dõi thiết bị (Device Tracker)
- ARP, Wireless, CAPsMAN, Netwatch
- DHCP leases → tự động tạo device tracker
- Phân giải tên thiết bị và nhà sản xuất (MAC vendor lookup)

### Hệ thống
- CPU, RAM, HDD, nhiệt độ, quạt, PSU
- UPS, GPS
- Firmware update (RouterOS + RouterBOARD)

### Khác
- Chạy script MikroTik
- Client traffic (Accounting v6 / Kid Control v7)
- PPP users, Captive Portal
- 26 ngôn ngữ (có tiếng Việt)
- Hỗ trợ nhiều thiết bị MikroTik cùng lúc

## Setup MikroTik

Tạo user cho Home Assistant trên MikroTik:

```
/user group add name=homeassistant policy=api,read,write,reboot,policy,test
/user add name=homeassistant group=homeassistant password=<mật-khẩu>
```

> **Lưu ý**: Quyền `api` và `read` là bắt buộc. Các quyền khác có thể giảm nhưng sẽ hạn chế tính năng.

## Setup Integration

1. Vào **Settings → Devices & Services → Add Integration**
2. Tìm **"Mikrotik Router"** (đừng nhầm với "Mikrotik" mặc định của HA)
3. Nhập thông tin:

| Trường | Giá trị |
|--------|---------|
| Name | Tên hiển thị |
| Host | IP MikroTik (vd: `192.168.10.1`) |
| Port | `0` (tự động: 8728 non-SSL / 8729 SSL) |
| Username | User đã tạo ở trên |
| Password | Mật khẩu |
| SSL | Bật nếu dùng port 8729 |

## Cấu hình (Options)

Ấn **Configure** trên integration để tùy chỉnh:

**Trang 1 — Basic:**
- Scan interval (giây)
- Theo dõi thiết bị trên interface
- Timeout device tracker
- Zone cho device tracker

**Trang 2 — Sensors:**
- Bật/tắt từng nhóm sensor và switch
- Filter switches, NAT, Mangle, PPP, Kid Control...

## Khác biệt so với upstream

| Mục | Upstream | Fork này |
|-----|----------|----------|
| Sửa lỗi | Đình trệ | 7+ lỗi critical đã sửa |
| HA tương thích | ≤2024.3 | 2024.3 → 2026.4 |
| librouteros | v3 | v3 + v4 |
| Hiệu năng | Gọi API không cần thiết | Skip query khi tính năng tắt |
| Phát triển | Ngừng hoạt động | Độc lập, đang phát triển |

## Development

```bash
git clone https://github.com/ngoviet/mikrotik-ha.git
cd mikrotik-ha

# Format & lint
black --check custom_components/
flake8 custom_components/
pylint --rcfile=setup.cfg custom_components/

# Test kết nối MikroTik
python -c "
from librouteros import connect
api = connect(host='192.168.10.1', username='admin', password='pass', port=8511)
print(list(api.path('/system/identity')))
api.close()
"
```

## License

Apache 2.0 — giữ nguyên từ upstream.
