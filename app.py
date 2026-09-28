import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# ==========================================
# 1. CẤU HÌNH TRANG & KHỞI TẠO DỮ LIỆU SẮP XẾP
# ==========================================
st.set_page_config(
    page_title="Hệ Thống Quản Lý Khách Sạn Professional",
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

# Đặt phòng mặc định mẫu
DEFAULT_BOOKINGS = [
    {
        "id": "BK-1001",
        "room_no": "102",
        "guest_name": "Nguyễn Văn A",
        "phone": "0901234567",
        "cccd": "012345678901",
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
        "cccd": "098765432109",
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
        {"date": "2026-09-25", "revenue": 3500000, "checkouts": 2},
        {"date": "2026-09-26", "revenue": 4200000, "checkouts": 3},
        {"date": "2026-09-27", "revenue": 2800000, "checkouts": 1},
    ])


# ==========================================
# 2. THANH THIẾT LẬP SIDEBAR & MENU
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2983/2983067.png", width=80)
st.sidebar.title("HOTEL MANAGEMENT")
st.sidebar.caption("Giải pháp Quản lý Vận hành & Doanh thu")

menu = st.sidebar.radio(
    "Điều hướng hệ thống:",
    [
        "📊 Tổng quan & KPI",
        "🗺️ Sơ đồ phòng",
        "🗝️ Nhận / Trả phòng (Check-in/out)",
        "🧹 Buồng phòng (Housekeeping)",
        "📈 Báo cáo doanh thu"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Mẹo Quản Lý:** Luôn đảm bảo phòng đạt trạng thái 'Sạch' trước khi bàn giao cho khách Check-in.")


# ==========================================
# 3. CHỨC NĂNG: TỔNG QUAN & KPI
# ==========================================
if menu == "📊 Tổng quan & KPI":
    st.title("📊 Tổng Quan Vận Hành Khách Sạn")
    
    df_rooms = st.session_state["rooms"]
    df_bookings = st.session_state["bookings"]
    
    total_rooms = len(df_rooms)
    occupied_rooms = len(df_rooms[df_rooms["status"] == "Đang có khách"])
    reserved_rooms = len(df_rooms[df_rooms["status"] == "Đã đặt"])
    available_rooms = len(df_rooms[df_rooms["status"] == "Trống"])
    maintenance_rooms = len(df_rooms[df_rooms["status"] == "Bảo trì"])
    
    occupancy_rate = (occupied_rooms / total_rooms) * 100 if total_rooms > 0 else 0
    
    # Hiển thị Chỉ số KPI chính
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Tổng số phòng", total_rooms)
    col2.metric("Đang có khách", occupied_rooms, f"{occupancy_rate:.1f}% Đầy")
    col3.metric("Phòng đã đặt", reserved_rooms)
    col4.metric("Phòng sẵn sàng", available_rooms)
    col5.metric("Đang bảo trì", maintenance_rooms)
    
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📌 Tỷ lệ Trạng thái Phòng")
        status_counts = df_rooms["status"].value_counts().reset_index()
        status_counts.columns = ["Trạng thái", "Số lượng"]
        
        fig_pie = px.pie(
            status_counts, 
            names="Trạng thái", 
            values="Số lượng", 
            hole=0.4,
            color="Trạng thái",
            color_discrete_map={
                "Trống": "#28a745",
                "Đang có khách": "#dc3545",
                "Đã đặt": "#ffc107",
                "Bảo trì": "#6c757d"
            }
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_chart2:
        st.subheader("🧹 Trạng thái Dọn dẹp Buồng phòng")
        hk_counts = df_rooms["housekeeping"].value_counts().reset_index()
        hk_counts.columns = ["Trạng thái Buồng", "Số lượng"]
        
        fig_bar = px.bar(
            hk_counts, 
            x="Trạng thái Buồng", 
            y="Số lượng", 
            color="Trạng thái Buồng",
            color_discrete_map={
                "Sạch": "#20c997",
                "Cần dọn": "#fd7e14",
                "Đang ở": "#17a2b8"
            }
        )
        st.plotly_chart(fig_bar, use_container_width=True)


# ==========================================
# 4. CHỨC NĂNG: SƠ ĐỒ PHÒNG TRỰC QUAN
# ==========================================
elif menu == "🗺️ Sơ đồ phòng":
    st.title("🗺️ Sơ Đồ Phòng Theo Tầng")
    
    df_rooms = st.session_state["rooms"]
    
    # Bộ lọc
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        floor_filter = st.multiselect("Lọc theo Tầng:", df_rooms["floor"].unique(), default=df_rooms["floor"].unique())
    with col_f2:
        status_filter = st.multiselect("Lọc theo Trạng thái:", df_rooms["status"].unique(), default=df_rooms["status"].unique())
        
    filtered_rooms = df_rooms[(df_rooms["floor"].isin(floor_filter)) & (df_rooms["status"].isin(status_filter))]
    
    # Color map cho từng trạng thái
    status_colors = {
        "Trống": "🟢 #d4edda",
        "Đang có khách": "🔴 #f8d7da",
        "Đã đặt": "🟡 #fff3cd",
        "Bảo trì": "⚪ #e2e3e5"
    }
    
    for floor in sorted(filtered_rooms["floor"].unique()):
        st.subheader(f"🏢 {floor}")
        rooms_in_floor = filtered_rooms[filtered_rooms["floor"] == floor]
        
        cols = st.columns(4)
        for idx, (_, room) in enumerate(rooms_in_floor.iterrows()):
            with cols[idx % 4]:
                color_bg = status_colors.get(room['status'], '#ffffff')
                st.markdown(
                    f"""
                    <div style="
                        border: 2px solid #ccc; 
                        border-radius: 10px; 
                        padding: 15px; 
                        margin-bottom: 15px;
                        background-color: {color_bg.split()[-1]};">
                        <h3 style="margin:0; color:#333;">Phòng {room['room_no']}</h3>
                        <p style="margin:5px 0;"><b>Loại:</b> {room['type']}</p>
                        <p style="margin:5px 0;"><b>Giá:</b> {room['price']:,} VNĐ</p>
                        <p style="margin:5px 0;"><b>Trạng thái:</b> {room['status']}</p>
                        <p style="margin:5px 0;"><b>Vệ sinh:</b> {room['housekeeping']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ==========================================
# 5. CHỨC NĂNG: CHECK-IN / CHECK-OUT
# ==========================================
elif menu == "🗝️ Nhận / Trả phòng (Check-in/out)":
    st.title("🗝️ Quản Lý Nhận & Trả Phòng")
    
    tab_checkin, tab_checkout, tab_history = st.tabs(["📥 Check-in (Nhận phòng)", "📤 Check-out (Trả phòng)", "📋 Danh sách lượt lưu trú"])
    
    df_rooms = st.session_state["rooms"]
    df_bookings = st.session_state["bookings"]
    
    # ---------------- TAB CHECK-IN ----------------
    with tab_checkin:
        st.subheader("Tạo lượt Nhận Phòng mới")
        
        # Chỉ chọn các phòng đang "Trống" và đã "Sạch"
        available_rooms_df = df_rooms[(df_rooms["status"] == "Trống") & (df_rooms["housekeeping"] == "Sạch")]
        
        if available_rooms_df.empty:
            st.warning("⚠️ Hiện không có phòng trống sẵn sàng (Cần kiểm tra trạng thái Vệ sinh hoặc Phòng trống).")
        else:
            with st.form("checkin_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    room_selected = st.selectbox("Chọn Phòng Trống:", available_rooms_df["room_no"].tolist())
                    guest_name = st.text_input("Họ và Tên Khách Hàng:")
                    phone = st.text_input("Số Điện Thoại:")
                    cccd = st.text_input("Số CCCD / Passport:")
                    
                with col2:
                    checkin_date = st.date_input("Ngày Check-in:", date.today())
                    checkout_date = st.date_input("Ngày Check-out Dự kiến:", date.today())
                    deposit = st.number_input("Tiền Cọc (VNĐ):", min_value=0, step=100000, value=200000)
                    
                btn_checkin = st.form_submit_button("✅ Xác Nhận Check-In")
                
                if btn_checkin:
                    if not guest_name or not phone:
                        st.error("Vui lòng điền đầy đủ tên và số điện thoại khách hàng.")
                    elif checkout_date <= checkin_date:
                        st.error("Ngày Check-out phải sau ngày Check-in ít nhất 1 ngày.")
                    else:
                        nights = (checkout_date - checkin_date).days
                        room_price = df_rooms[df_rooms["room_no"] == room_selected]["price"].values[0]
                        total_price = (nights * room_price)
                        
                        # Tạo booking mới
                        new_booking = {
                            "id": f"BK-{len(df_bookings) + 1001}",
                            "room_no": room_selected,
                            "guest_name": guest_name,
                            "phone": phone,
                            "cccd": cccd,
                            "checkin": checkin_date,
                            "checkout": checkout_date,
                            "service_fee": 0,
                            "deposit": deposit,
                            "total": total_price,
                            "status": "Đang ở"
                        }
                        
                        # Cập nhật danh sách Booking & Trạng thái phòng
                        st.session_state["bookings"] = pd.concat([df_bookings, pd.DataFrame([new_booking])], ignore_index=True)
                        st.session_state["rooms"].loc[st.session_state["rooms"]["room_no"] == room_selected, "status"] = "Đang có khách"
                        st.session_state["rooms"].loc[st.session_state["rooms"]["room_no"] == room_selected, "housekeeping"] = "Đang ở"
                        
                        st.success(f"🎉 Check-in thành công phòng {room_selected} cho khách {guest_name}!")
                        st.rerun()

    # ---------------- TAB CHECK-OUT ----------------
    with tab_checkout:
        st.subheader("Thanh toán & Trả Phòng")
        
        active_bookings = df_bookings[df_bookings["status"] == "Đang ở"]
        
        if active_bookings.empty:
            st.info("Hiện tại không có phòng nào đang có khách lưu trú.")
        else:
            selected_booking_id = st.selectbox(
                "Chọn lượt phòng trả:",
                active_bookings["id"].tolist(),
                format_func=lambda x: f"Mã {x} - Phòng {active_bookings[active_bookings['id']==x]['room_no'].values[0]} ({active_bookings[active_bookings['id']==x]['guest_name'].values[0]})"
            )
            
            booking_info = active_bookings[active_bookings["id"] == selected_booking_id].iloc[0]
            room_info = df_rooms[df_rooms["room_no"] == booking_info["room_no"]].iloc[0]
            
            # Tính toán số đêm thực tế
            nights = (booking_info["checkout"] - booking_info["checkin"]).days
            nights = max(nights, 1) # Ít nhất 1 đêm
            room_charge = nights * room_info["price"]
            
            st.markdown("---")
            st.write("### 🧾 Hóa Đơn Thanh Toán")
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                st.write(f"**Khách hàng:** {booking_info['guest_name']}")
                st.write(f"**Số điện thoại:** {booking_info['phone']}")
                st.write(f"**Số phòng:** {booking_info['room_no']} ({room_info['type']})")
                st.write(f"**Thời gian:** {booking_info['checkin']} ➔ {booking_info['checkout']} ({nights} đêm)")
                
            with col_b2:
                service_fee = st.number_input("Phụ thu / Chi phí dịch vụ phát sinh (VNĐ):", min_value=0, value=int(booking_info["service_fee"]), step=50000)
                deposit = booking_info["deposit"]
                grand_total = room_charge + service_fee
                final_pay = grand_total - deposit
                
                st.write(f"**Tiền phòng:** {room_charge:,} VNĐ")
                st.write(f"**Đã đặt cọc:** -{deposit:,} VNĐ")
                st.markdown(f"### **Còn lại phải thanh toán:** :green[{final_pay:,} VNĐ]")
                
            if st.button("🔔 Xác Nhận Check-Out & Xuất Hóa Đơn"):
                # Cập nhật booking status
                st.session_state["bookings"].loc[st.session_state["bookings"]["id"] == selected_booking_id, "status"] = "Đã trả phòng"
                st.session_state["bookings"].loc[st.session_state["bookings"]["id"] == selected_booking_id, "service_fee"] = service_fee
                st.session_state["bookings"].loc[st.session_state["bookings"]["id"] == selected_booking_id, "total"] = grand_total
                
                # Cập nhật phòng -> Trống & Cần dọn
                st.session_state["rooms"].loc[st.session_state["rooms"]["room_no"] == booking_info["room_no"], "status"] = "Trống"
                st.session_state["rooms"].loc[st.session_state["rooms"]["room_no"] == booking_info["room_no"], "housekeeping"] = "Cần dọn"
                
                # Cập nhật lịch sử doanh thu
                today_str = date.today().strftime("%Y-%m-%d")
                df_rev = st.session_state["revenue_history"]
                if today_str in df_rev["date"].values:
                    st.session_state["revenue_history"].loc[df_rev["date"] == today_str, "revenue"] += grand_total
                    st.session_state["revenue_history"].loc[df_rev["date"] == today_str, "checkouts"] += 1
                else:
                    new_rev = pd.DataFrame([{"date": today_str, "revenue": grand_total, "checkouts": 1}])
                    st.session_state["revenue_history"] = pd.concat([df_rev, new_rev], ignore_index=True)
                    
                st.balloons()
                st.success(f"Khách hàng {booking_info['guest_name']} đã hoàn tất trả phòng {booking_info['room_no']}!")
                st.rerun()

    # ---------------- TAB DỮ LIỆU LƯU TRÚ ----------------
    with tab_history:
        st.subheader("📋 Tất cả đơn đặt phòng")
        st.dataframe(st.session_state["bookings"], use_container_width=True)


# ==========================================
# 6. CHỨC NĂNG: BUỒNG PHÒNG (HOUSEKEEPING)
# ==========================================
elif menu == "🧹 Buồng phòng (Housekeeping)":
    st.title("🧹 Quản Lý Dọn Dẹp Buồng Phòng")
    st.caption("Cập nhật tình trạng vệ sinh thực tế để đảm bảo chất lượng phục vụ khách hàng.")
    
    df_rooms = st.session_state["rooms"]
    
    edited_df = st.data_editor(
        df_rooms[["room_no", "floor", "type", "status", "housekeeping"]],
        column_config={
            "room_no": st.column_config.TextColumn("Số phòng", disabled=True),
            "floor": st.column_config.TextColumn("Tầng", disabled=True),
            "type": st.column_config.TextColumn("Loại phòng", disabled=True),
            "status": st.column_config.TextColumn("Trạng thái phòng", disabled=True),
            "housekeeping": st.column_config.SelectboxColumn(
                "Trạng thái Buồng",
                options=["Sạch", "Cần dọn", "Đang ở"],
                required=True
            )
        },
        hide_index=True,
        use_container_width=True
    )
    
    if st.button("💾 Lưu Cập Nhật Trạng Thái Dọn Phòng"):
        st.session_state["rooms"]["housekeeping"] = edited_df["housekeeping"]
        st.success("Đã cập nhật trạng thái buồng phòng thành công!")
        st.rerun()


# ==========================================
# 7. CHỨC NĂNG: BÁO CÁO DOANH THU
# ==========================================
elif menu == "📈 Báo cáo doanh thu":
    st.title("📈 Báo Cáo Doanh Thu & Hiệu Quả Vận Hành")
    
    df_rev = st.session_state["revenue_history"]
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        total_rev = df_rev["revenue"].sum()
        st.metric("Tổng Doanh Thu Ghi Nhận", f"{total_rev:,} VNĐ")
    with col_r2:
        total_co = df_rev["checkouts"].sum()
        st.metric("Tổng Lượt Check-out", f"{total_co} Lượt")
        
    st.markdown("---")
    st.subheader("📉 Biểu đồ doanh thu theo ngày")
    
    fig_rev = px.line(
        df_rev, 
        x="date", 
        y="revenue", 
        markers=True,
        title="Xu Hướng Doanh Thu Thu Được Qua Các Ngày",
        labels={"date": "Ngày", "revenue": "Doanh thu (VNĐ)"}
    )
    st.plotly_chart(fig_rev, use_container_width=True)
    
    st.subheader("📋 Chi tiết nhật ký doanh thu")
    st.dataframe(df_rev, use_container_width=True)
