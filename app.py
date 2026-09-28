import streamlit as st
import pandas as pd
from datetime import date

# ==========================================
# 1. CẤU HÌNH TRANG & DỮ LIỆU BAN ĐẦU
# ==========================================
st.set_page_config(
    page_title="Hệ Thống Quản Lý Khách Sạn",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Danh sách phòng mặc định
DEFAULT_ROOMS = [
    {"room_no": "101", "floor": "Tầng 1", "type": "Standard", "price": 500000, "status": "Trống", "housekeeping": "Sạch"},
    {"room_no": "102", "floor": "Tầng 1", "type": "Standard", "price": 500000, "status": "Đang có khách", "housekeeping": "Đang ở"},
    {"room_no": "103", "floor": "Tầng 1", "type": "Superior", "price": 750000, "status": "Trống", "housekeeping": "Cần dọn"},
    {"room_no": "201", "floor": "Tầng 2", "type": "Superior", "price": 750000, "status": "Trống", "housekeeping": "Sạch"},
    {"room_no": "202", "floor": "Tầng 2", "type": "Deluxe", "price": 1200000, "status": "Đang có khách", "housekeeping": "Đang ở"},
    {"room_no": "203", "floor": "Tầng 2", "type": "Deluxe", "price": 1200000, "status": "Bảo trì", "housekeeping": "Cần dọn"},
    {"room_no": "301", "floor": "Tầng 3", "type": "VIP Suite", "price": 2000000, "status": "Trống", "housekeeping": "Sạch"},
    {"room_no": "302", "floor": "Tầng 3", "type": "VIP Suite", "price": 2000000, "status": "Đã đặt", "housekeeping": "Sạch"},
]

# Đặt phòng mẫu
DEFAULT_BOOKINGS = [
    {
        "id": "BK-1001",
        "room_no": "102",
        "guest_name": "Nguyễn Văn A",
        "phone": "0901234567",
        "checkin": date(2026, 9, 27),
        "checkout": date(2026, 9, 29),
        "service_fee": 150000,
        "deposit": 500000,
        "total": 1150000,
        "status": "Đang ở"
    },
    {
        "id": "BK-1002",
        "room_no": "202",
        "guest_name": "Trần Thị B",
        "phone": "0987654321",
        "checkin": date(2026, 9, 26),
        "checkout": date(2026, 9, 28),
        "service_fee": 300000,
        "deposit": 1000000,
        "total": 2700000,
        "status": "Đang ở"
    }
]

# Lưu trữ Session State
if "rooms" not in st.session_state:
    st.session_state["rooms"] = pd.DataFrame(DEFAULT_ROOMS)

if "bookings" not in st.session_state:
    st.session_state["bookings"] = pd.DataFrame(DEFAULT_BOOKINGS)

if "revenue_history" not in st.session_state:
    st.session_state["revenue_history"] = pd.DataFrame([
        {"Ngày": "2026-09-25", "Doanh thu": 3500000},
        {"Ngày": "2026-09-26", "Doanh thu": 4200000},
        {"Ngày": "2026-09-27", "Doanh thu": 2800000},
    ])


# ==========================================
# 2. THANH THIẾT LẬP SIDEBAR & MENU
# ==========================================
st.sidebar.title("🏨 KHÁCH SẠN PRO")
st.sidebar.caption("Hệ thống Quản lý Vận hành")

menu = st.sidebar.radio(
    "Danh mục quản lý:",
    [
        "📊 Tổng quan & KPI",
        "🗺️ Sơ đồ phòng",
        "🗝️ Nhận / Trả phòng",
        "🧹 Buồng phòng",
        "📈 Báo cáo doanh thu"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Phiên bản 2.0 - Tối ưu hoá hệ thống")


# ==========================================
# 3. MÀN HÌNH: TỔNG QUAN & KPI
# ==========================================
if menu == "📊 Tổng quan & KPI":
    st.title("📊 Tổng Quan Vận Hành Khách Sạn")
    
    df_rooms = st.session_state["rooms"]
    
    total_rooms = len(df_rooms)
    occupied_rooms = len(df_rooms[df_rooms["status"] == "Đang có khách"])
    reserved_rooms = len(df_rooms[df_rooms["status"] == "Đã đặt"])
    available_rooms = len(df_rooms[df_rooms["status"] == "Trống"])
    maintenance_rooms = len(df_rooms[df_rooms["status"] == "Bảo trì"])
    
    occupancy_rate = (occupied_rooms / total_rooms) * 100 if total_rooms > 0 else 0
    
    # Chỉ số KPI
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Tổng số phòng", total_rooms)
    col2.metric("Đang có khách", occupied_rooms, f"{occupancy_rate:.1f}% Đầy")
    col3.metric("Phòng đã đặt", reserved_rooms)
    col4.metric("Phòng sẵn sàng", available_rooms)
    col5.metric("Đang bảo trì", maintenance_rooms)
    
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📌 Thống kê trạng thái phòng")
        status_df = df_rooms["status"].value_counts().reset_index()
        status_df.columns = ["Trạng thái", "Số lượng"]
        st.bar_chart(status_df.set_index("Trạng thái"))
        
    with col_chart2:
        st.subheader("🧹 Thống kê tình trạng vệ sinh")
        hk_df = df_rooms["housekeeping"].value_counts().reset_index()
        hk_df.columns = ["Vệ sinh", "Số lượng"]
        st.bar_chart(hk_df.set_index("Vệ sinh"))


# ==========================================
# 4. MÀN HÌNH: SƠ ĐỒ PHÒNG TRỰC QUAN
# ==========================================
elif menu == "🗺️ Sơ đồ phòng":
    st.title("🗺️ Sơ Đồ Phòng Khách Sạn")
    
    df_rooms = st.session_state["rooms"]
    
    # Bộ lọc
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        floor_filter = st.multiselect("Chọn Tầng:", df_rooms["floor"].unique(), default=df_rooms["floor"].unique())
    with col_f2:
        status_filter = st.multiselect("Chọn Trạng thái:", df_rooms["status"].unique(), default=df_rooms["status"].unique())
        
    filtered_rooms = df_rooms[(df_rooms["floor"].isin(floor_filter)) & (df_rooms["status"].isin(status_filter))]
    
    status_bg = {
        "Trống": "#d4edda",
        "Đang có khách": "#f8d7da",
        "Đã đặt": "#fff3cd",
        "Bảo trì": "#e2e3e5"
    }
    
    for floor in sorted(filtered_rooms["floor"].unique()):
        st.subheader(f"🏢 {floor}")
        rooms_in_floor = filtered_rooms[filtered_rooms["floor"] == floor]
        
        cols = st.columns(4)
        for idx, (_, room) in enumerate(rooms_in_floor.iterrows()):
            with cols[idx % 4]:
                bg_color = status_bg.get(room['status'], '#ffffff')
                st.markdown(
                    f"""
                    <div style="
                        border: 1px solid #ccc; 
                        border-radius: 8px; 
                        padding: 12px; 
                        margin-bottom: 12px;
                        background-color: {bg_color};">
                        <h3 style="margin:0; color:#333;">Phòng {room['room_no']}</h3>
                        <p style="margin:4px 0;"><b>Loại:</b> {room['type']}</p>
                        <p style="margin:4px 0;"><b>Giá:</b> {room['price']:,} VNĐ</p>
                        <p style="margin:4px 0;"><b>Trạng thái:</b> {room['status']}</p>
                        <p style="margin:4px 0;"><b>Vệ sinh:</b> {room['housekeeping']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ==========================================
# 5. MÀN HÌNH: CHECK-IN / CHECK-OUT
# ==========================================
elif menu == "🗝️ Nhận / Trả phòng":
    st.title("🗝️ Quản Lý Nhận & Trả Phòng")
    
    tab_checkin, tab_checkout, tab_history = st.tabs(["📥 Check-in", "📤 Check-out", "📋 Danh sách lưu trú"])
    
    df_rooms = st.session_state["rooms"]
    df_bookings = st.session_state["bookings"]
    
    # --- CHECK-IN ---
    with tab_checkin:
        st.subheader("Nhận phòng mới")
        available_rooms_df = df_rooms[(df_rooms["status"] == "Trống") & (df_rooms["housekeeping"] == "Sạch")]
        
        if available_rooms_df.empty:
            st.warning("⚠️ Không có phòng trống sẵn sàng. Lễ tân cần kiểm tra lại sơ đồ phòng hoặc lịch vệ sinh.")
        else:
            with st.form("checkin_form"):
                col1, col2 = st.columns(2)
                with col1:
                    room_selected = st.selectbox("Chọn Phòng Trống:", available_rooms_df["room_no"].tolist())
                    guest_name = st.text_input("Tên Khách Hàng:")
                    phone = st.text_input("Số Điện Thoại:")
                with col2:
                    checkin_date = st.date_input("Ngày Check-in:", date.today())
                    checkout_date = st.date_input("Ngày Check-out Dự kiến:", date.today())
                    deposit = st.number_input("Tiền Cọc (VNĐ):", min_value=0, step=100000, value=200000)
                    
                btn_checkin = st.form_submit_button("✅ Xác Nhận Check-In")
                
                if btn_checkin:
                    if not guest_name or not phone:
                        st.error("Vui lòng điền tên và số điện thoại khách hàng.")
                    elif checkout_date <= checkin_date:
                        st.error("Ngày trả phòng phải sau ngày nhận phòng.")
                    else:
                        nights = (checkout_date - checkin_date).days
                        room_price = df_rooms[df_rooms["room_no"] == room_selected]["price"].values[0]
                        total_price = nights * room_price
                        
                        new_booking = {
                            "id": f"BK-{len(df_bookings) + 1001}",
                            "room_no": room_selected,
                            "guest_name": guest_name,
                            "phone": phone,
                            "checkin": checkin_date,
                            "checkout": checkout_date,
                            "service_fee": 0,
                            "deposit": deposit,
                            "total": total_price,
                            "status": "Đang ở"
                        }
                        
                        st.session_state["bookings"] = pd.concat([df_bookings, pd.DataFrame([new_booking])], ignore_index=True)
                        st.session_state["rooms"].loc[st.session_state["rooms"]["room_no"] == room_selected, "status"] = "Đang có khách"
                        st.session_state["rooms"].loc[st.session_state["rooms"]["room_no"] == room_selected, "housekeeping"] = "Đang ở"
                        
                        st.success(f"Khách {guest_name} nhận phòng {room_selected} thành công!")
                        st.rerun()

    # --- CHECK-OUT ---
    with tab_checkout:
        st.subheader("Thanh toán & Trả phòng")
        active_bookings = df_bookings[df_bookings["status"] == "Đang ở"]
        
        if active_bookings.empty:
            st.info("Hiện không có phòng nào cần trả.")
        else:
            selected_booking_id = st.selectbox(
                "Chọn lượt trả phòng:",
                active_bookings["id"].tolist(),
                format_func=lambda x: f"Mã {x} - Phòng {active_bookings[active_bookings['id']==x]['room_no'].values[0]} ({active_bookings[active_bookings['id']==x]['guest_name'].values[0]})"
            )
            
            booking_info = active_bookings[active_bookings["id"] == selected_booking_id].iloc[0]
            room_info = df_rooms[df_rooms["room_no"] == booking_info["room_no"]].iloc[0]
            
            nights = max((booking_info["checkout"] - booking_info["checkin"]).days, 1)
            room_charge = nights * room_info["price"]
            
            st.markdown("---")
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                st.write(f"**Khách hàng:** {booking_info['guest_name']}")
                st.write(f"**SĐT:** {booking_info['phone']}")
                st.write(f"**Số phòng:** {booking_info['room_no']}")
                st.write(f"**Thời gian:** {booking_info['checkin']} ➔ {booking_info['checkout']} ({nights} đêm)")
            with col_b2:
                service_fee = st.number_input("Phụ thu dịch vụ (VNĐ):", min_value=0, value=int(booking_info["service_fee"]), step=50000)
                deposit = booking_info["deposit"]
                grand_total = room_charge + service_fee
                final_pay = grand_total - deposit
                
                st.write(f"**Tiền phòng:** {room_charge:,} VNĐ")
                st.write(f"**Đã cọc:** -{deposit:,} VNĐ")
                st.markdown(f"### **Thanh toán còn lại:** :green[{final_pay:,} VNĐ]")
                
            if st.button("🔔 Hoàn Tất Trả Phòng"):
                st.session_state["bookings"].loc[st.session_state["bookings"]["id"] == selected_booking_id, "status"] = "Đã trả phòng"
                st.session_state["bookings"].loc[st.session_state["bookings"]["id"] == selected_booking_id, "service_fee"] = service_fee
                st.session_state["bookings"].loc[st.session_state["bookings"]["id"] == selected_booking_id, "total"] = grand_total
                
                st.session_state["rooms"].loc[st.session_state["rooms"]["room_no"] == booking_info["room_no"], "status"] = "Trống"
                st.session_state["rooms"].loc[st.session_state["rooms"]["room_no"] == booking_info["room_no"], "housekeeping"] = "Cần dọn"
                
                today_str = date.today().strftime("%Y-%m-%d")
                df_rev = st.session_state["revenue_history"]
                if today_str in df_rev["Ngày"].values:
                    st.session_state["revenue_history"].loc[df_rev["Ngày"] == today_str, "Doanh thu"] += grand_total
                else:
                    new_rev = pd.DataFrame([{"Ngày": today_str, "Doanh thu": grand_total}])
                    st.session_state["revenue_history"] = pd.concat([df_rev, new_rev], ignore_index=True)
                    
                st.success("Trả phòng thành công!")
                st.rerun()

    # --- DANH SÁCH LƯU TRÚ ---
    with tab_history:
        st.subheader("📋 Toàn bộ dữ liệu đặt phòng")
        st.dataframe(st.session_state["bookings"], use_container_width=True)


# ==========================================
# 6. MÀN HÌNH: BUỒNG PHÒNG
# ==========================================
elif menu == "🧹 Buồng phòng":
    st.title("🧹 Quản Lý Dọn Dẹp Buồng Phòng")
    
    df_rooms = st.session_state["rooms"]
    
    edited_df = st.data_editor(
        df_rooms[["room_no", "floor", "type", "status", "housekeeping"]],
        column_config={
            "room_no": st.column_config.TextColumn("Số phòng", disabled=True),
            "floor": st.column_config.TextColumn("Tầng", disabled=True),
            "type": st.column_config.TextColumn("Loại phòng", disabled=True),
            "status": st.column_config.TextColumn("Trạng thái phòng", disabled=True),
            "housekeeping": st.column_config.SelectboxColumn(
                "Tình trạng vệ sinh",
                options=["Sạch", "Cần dọn", "Đang ở"],
                required=True
            )
        },
        hide_index=True,
        use_container_width=True
    )
    
    if st.button("💾 Lưu Trạng Thái Vệ Sinh"):
        st.session_state["rooms"]["housekeeping"] = edited_df["housekeeping"]
        st.success("Cập nhật thành công!")
        st.rerun()


# ==========================================
# 7. MÀN HÌNH: BÁO CÁO DOANH THU
# ==========================================
elif menu == "📈 Báo cáo doanh thu":
    st.title("📈 Báo Cáo Doanh Thu")
    
    df_rev = st.session_state["revenue_history"]
    
    total_rev = df_rev["Doanh thu"].sum()
    st.metric("Tổng Doanh Thu Lấy Được", f"{total_rev:,} VNĐ")
    
    st.markdown("---")
    st.subheader("📉 Biểu đồ xu hướng doanh thu")
    
    # Biểu đồ dòng nguyên bản Streamlit
    chart_data = df_rev.set_index("Ngày")
    st.line_chart(chart_data)
    
    st.subheader("📋 Chi tiết nhật ký")
    st.dataframe(df_rev, use_container_width=True)
