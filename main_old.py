import flet as ft
import firebase
from flet import *
from firebase import firebase 
# for Check WIFI
import requests
# import psutil
import threading
import time
# 

def main(page: Page):
    page.title ="ควบคุมปิด-เปิด ประตูหน้าแผนกวิชาช่างอิเล็กทรอนิกส์ วิทยาลัยเทตนิคกำแพงเพชร" 
    firebase_app=""
    data  =""
        # Function to check Wi-Fi connection status
    def check_wifi_connection():   
        try:
            response = requests.get("https://www.google.com/", timeout=2)
            return True
        except requests.ConnectionError:
            return False    

    # Function to update Wi-Fi status in the UI
    def update_wifi_status(page, wifi_status):
        if check_wifi_connection():
            wifi_status.value = "Status: Ready..."
            wifi_status.color = ft.Colors.GREEN
            
        else:
            wifi_status.value = "Status: Disconnected"
            wifi_status.color = ft.Colors.RED
        page.update()

    # Function to run the Wi-Fi status update periodically
    def start_wifi_status_update(form, wifi_status):
        def run():
            while True:
                time.sleep(2)  # Wait for 5 seconds
                update_wifi_status(form, wifi_status)
        threading.Thread(target=run, daemon=True).start()  
      
      
      
       
    def checkbox_changed(e):
        print(f"Save User:{username.value},Pass:{password.value}")
        page.update()
        
    # Wi-Fi connection status
    wifi_status = Text(value="Status:  Checking...", color=ft.Colors.ORANGE,size=25)    
    if check_wifi_connection():
        firebase_app = firebase.FirebaseApplication('https://electronicsdoor-501-default-rtdb.firebaseio.com/',None)    
        data = firebase_app.get('Users', '')
        
        # data_Home = firebase_app.get('smart-home/living room', '')
        # print(f"data:{data_Home}")
        # for user_data in data_Home.items():            
        #     if user_data['Fan1']=="on" :
        #         sw[0].selected=True
        #     else:sw[0].selected=False 
        #     if user_data['Lamp1']=="on" :
        #         sw[1].selected=True
        #     else:sw[1].selected=False 
        #     if user_data['Lamp2']=="on" :
        #         sw[2].selected=True
        #     else:sw[2].selected=False 
        #     if user_data['Lamp3']=="on" :
        #         sw[3].selected=True
        #     else:sw[3].selected=False 
                                                   
    
    username = TextField(
            hint_text="Username",
                            icon=ft.Icons.PERSON_ROUNDED,     
                            border_color="transparent",
                            bgcolor="transparent",
                            content_padding=2,
                            cursor_color="blue",
                            cursor_width=1,
                            color="blue",      
        )
        
    password = TextField(
            hint_text="Password",
                            icon=ft.Icons.LOCK_OUTLINE_ROUNDED,                            
                            border_color="transparent",
                            bgcolor="transparent",
                            text_size=16,
                            content_padding=3,
                            cursor_color="blue",
                            cursor_width=1,
                            color="blue",
                           password=True,
                            can_reveal_password=True 
        )    
    def toggle_icon_button(e):
        e.control.selected = not e.control.selected
        LampValue={}
        for i in range(8):
            if sw[i].selected :
                # firebase_app.post('/smart-home',{'Lamp1': 'on'})
                LampValue[i]='on'                                   
            else:          
                LampValue[i]='off'
            
        print(f"switch:{sw[0].selected},{sw[1].selected}, {sw[2].selected},{sw[3].selected},{sw[4].selected},{sw[5].selected},{sw[6].selected},{sw[7].selected}")
        # Sent Data to /smart-home/bedroom
        firebase_app.put('/smart-home','Door',{
            "Sw1": LampValue[0],
            "pause1": LampValue[1],
            "Sw2": LampValue[2],
            "pause2": LampValue[3]         
            
            })
        
             
        
        # Sent Data to /smart-home','women
        # firebase_app.put('/smart-home','women',{
        #     "Sw1": LampValue[0],
        #     "pause": LampValue[1]                     
        #     })
        
        # e.control.update()
    
    Sw1=Text(
        "ชาย",
        size=16,
        weight="w700",color="white",
    )
    Sw2=Text(
        "หญิง",
        size=16,
        weight="w700",color="white",
    )
    pause=Text(
        "หยุด",
        size=16,
        weight="w700",color="white",
    )
    
        
    sw={}   
    for i in range(8) :   
        sw[i]=ft.IconButton(
                            
                            icon_size=45,
                            icon=ft.Icons.POWER_SETTINGS_NEW,
                            bgcolor="WHITE70",
                            # selected_icon=ft.Icons.POWER_SETTINGS_NEW,                            
                            selected_icon=ft.Icons.POWER_SETTINGS_NEW,  
                            on_click=toggle_icon_button,
                            # selected=False,
                            style=ft.ButtonStyle(color={"selected": ft.Colors.GREEN, "": ft.Colors.RED}),
                         )
    
    door1_Sw1=Container(
        width=150,
        height=70,
        bgcolor=ft.Colors.BLUE_GREY,
        border_radius=10,
        content=Row(
            controls=[
                sw[0],
                Sw1,                
            ]               
        )
    )        
    door1_pause=Container(
        width=150,
        height=70,
        bgcolor=ft.Colors.BLUE_GREY,
        border_radius=10,
        content=Row(
            controls=[
                sw[1],
                pause,                
            ]               
        )
    )
    door2_sw1=Container(
                width=150,
                height=70,
                bgcolor=ft.Colors.BLUE_GREY,
                border_radius=10,
                content=Row(
                controls=[
                sw[2],
                Sw2,                
                            ]               
                        )
                    )
    door2_pause=Container(
        width=150,
        height=70,
        bgcolor=ft.Colors.BLUE_GREY,
        border_radius=10,
        content=Row(
            controls=[
                sw[3],
                pause,                
            ]               
        )
    )
   
    def Signin_bt(e):
        if check_wifi_connection():
            for user_id, user_data in data.items():
                # print(f"Save User:{user_data['name']},Pass:{user_data['password']}")
                if user_data['name']==username.value and user_data['password']==password.value:
                    UpdateKey()
                    page.go("/Page_Home")
                        
                if user_data['name']!=username.value or user_data['password']!=password.value:
                    username.helper_text="เอ้าเฮ้ย"
                    password.helper_text="ไอหย่า"
                    page.update()    
    
    def clear_scr(e):
        page.go("/")
        username.helper_text=""
        password.helper_text=""
        username.value=""
        password.value=""
        page.update()
        
    def clear_user(e): 
        username.helper_text=""
        password.helper_text=""
        username.value=""
        password.value=""
        page.update()
        
    def Login_page(e): 
        page.go("/")
        username.helper_text=""
        password.helper_text=""
       
        page.update() 
        
    def UpdateKey():
        # Data For smart-home/living room
        data_Home = firebase_app.get('smart-home/Door', '')
        
        for key in data_Home:     
            print(f"{key}:{data_Home[key]}")       
            if key=='Sw1' and data_Home[key]=="on" :
                sw[0].selected=True
            elif key=='Sw1' and data_Home[key]=="off" : 
                sw[0].selected=False             
            if key=='pause1' and data_Home[key]=="on":
                sw[1].selected=True
            elif key=='pause1' and data_Home[key]=="off":
                sw[1].selected=False 
            if key=='Sw2' and data_Home[key]=="on" :
                sw[2].selected=True
            elif key=='Sw2' and data_Home[key]=="off":
                sw[2].selected=False 
            if key=='pause2' and data_Home[key]=="on":
                sw[3].selected=True
            elif key=='pause2' and data_Home[key]=="off":
                sw[3].selected=False  
                
        #         #Data For /smart-home/bedroom
        # data_Home = firebase_app.get('/smart-home/bedroom', '')
        
        # for key in data_Home:     
        #     print(f"{key}:{data_Home[key]}")       
        #     if key=='Air1' and data_Home[key]=="on" :
        #         sw[4].selected=True
        #     elif key=='Air1' and data_Home[key]=="off" : 
        #         sw[4].selected=False             
        #     if key=='Lamp1' and data_Home[key]=="on":
        #         sw[5].selected=True
        #     elif key=='Lamp1' and data_Home[key]=="off":
        #         sw[5].selected=False 
        #     if key=='Lamp2' and data_Home[key]=="on" :
        #         sw[6].selected=True
        #     elif key=='Lamp2' and data_Home[key]=="off":
        #         sw[6].selected=False 
            
        # # Data for /smart-home/bathroom               # 
        # data_Home = firebase_app.get('/smart-home/bathroom', '')
        
        # for key in data_Home:     
                  
        #     if key=='Lamp1' and data_Home[key]=="on":
        #         sw[7].selected=True
        #     elif key=='Lamp1' and data_Home[key]=="off":
        #         sw[7].selected=False 
            
       
        # print(f"switch:{sw[0].selected},{sw[1].selected}, {sw[2].selected},{sw[3].selected},{sw[4].selected},{sw[5].selected},{sw[6].selected},{sw[7].selected}")
        page.update() 
  
    def button_clicked(e):        
        
        # elif(e.control.selected_index==1):
        #     page.go("/Page_LIGHT_MODE")
        # elif(e.control.selected_index==2):
        #     page.go("/Page_Temperature")
        if(e.control.selected_index==0):
            page.go("/")
            username.helper_text=""
            password.helper_text=""
            username.value=""
            password.value=""    
            # page.update()        
        else:
            
            page.go("/Page_Home")   
                   
        page.update()  
    
    Bt_Home=Text(                       
                         style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),                       
                        bgcolor="GREY",
                        color="white",
                        width=200,
                        height=55,
                        
                        # opacity_on_click=0.3,
                        
                       )  
    
    MenuTemplat=ft.NavigationBar(
          
                        # on_change=lambda e: print("Selected tab:", e.control.selected_index), 
                        on_change=button_clicked, 
                        destinations=[
                            # ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Explore"),
                            # ft.NavigationBarDestination(icon=ft.Icons.LIGHT_MODE, label="ระบบแสงสว่าง",tooltip="ระบบแสงสว่าง"),
                            # ft.NavigationBarDestination(icon=ft.Icons.THERMOSTAT_SHARP,label="ควบคุมอุณหภูมิ",tooltip="ระบบควบคุมอุณหภูมิ"),
                            # ft.NavigationBarDestination(icon=ft.Icons.PERSON,label="Profile"),
                            # ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
                            ft.NavigationBarDestination(icon=ft.Icons.LOGOUT,label="Logout" ),
                        ]
                    )    
    
    # form        
        
    form = Card(
            width=450,
            height=500,
            elevation=5,
            content=Container(
                bgcolor="gray" ,#23262a",
                border_radius=6,
                content=Column(
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Divider(height=1, color="transparent"),
                        
                        Container(
                            content=wifi_status,
                            margin=1,
                            padding=2,
                            alignment=ft.alignment.center,
                            width=450,
                            height=50,
                            # border_radius=8,
                            # border=border.all(3,"blue" ), 
                            ink=True,
                            # bgcolor= "blue" ,
                        ),
                    
                        Divider(height=1, color="transparent"),
                        Stack(
                            controls=[
                          
                            Icon(name=Icons.HOME_ROUNDED, color=ft.Colors.BLUE, size=100),
                             ],
                        ),
                     
                        Divider(height=3, color="transparent"),
                     
                        Container(
                            content=username,
                            margin=1,
                            padding=2,
                            alignment=ft.alignment.center,
                            width=250,
                            height=50,
                            border_radius=8,
                            border=border.all(3,"blue" ), 
                            ink=True,
                        ),
                    
                        Divider(height=1, color="transparent"),

                        Container(
                            content=password,
                            margin=1,
                            padding=1,
                            alignment=ft.alignment.center,
                            width=250,
                            height=50,
                            border_radius=8,
                            border=border.all(3,"blue" ), 
                            ink=True,
                            ),
                    
                       
                        Divider(height=1, color="transparent"),
                        Row(
                            width=320,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                             
                                Checkbox(value=False, 
                                         on_change=checkbox_changed,
                                        fill_color="blue"
                                        ),
                                Text("Remember me", size=12,color="blue"),
                                # Text("Forgot Passowrd?", size=12,color="blue"),
                                                               
                            ],
                        ),
                        Divider(height=1, color="transparent"),                                            
                        ft.CupertinoFilledButton(
                        content=ft.Text("LOGIN"),
                        opacity_on_click=0.3,
                        # on_click=lambda e: print(f"LOGIN! {username.value},{password.value}"),
                        on_click= Signin_bt,
                        width=250,
                        height=50,
                    ),
                        Divider(height=35, color="transparent"),
                        
                    ],
                ),
            ),
        )    
    
    def route_change(route):
       
        page.views.clear()
        page.views.append(
            
            View(
                "/" ,
                [
                  form
                ],
                vertical_alignment= "center" ,
                horizontal_alignment= "center",
                bgcolor = "#212328"  
            )
        )
        if page.route == "/Page_Home":
            page.views.append(
                ft.View(
                    "/Page_Home",
                    [
                        Divider(height=5, color="transparent"),
                        Text(" ควบคุม ปิด-เปิด ประตูแผนกวิชาช่างอิเล็กทรอนิกส์",size=22,color="blue"),
                        #  Divider(height=5, color="transparent"),
                       Icon(name=Icons.HOME_OUTLINED,  size=150),
                       Divider(height=5, color="transparent"),
                        
                        ft.Row(
                            controls=[door1_Sw1,door1_pause] ,
                             alignment=ft.MainAxisAlignment.CENTER,                                                                           
                        ),
                        Divider(height=5, color="transparent"),
                        ft.Row(
                            controls=[door2_sw1,door2_pause] ,
                             alignment=ft.MainAxisAlignment.CENTER,                                                                           
                        ),
                     MenuTemplat,
        
                    ],
                    vertical_alignment= "top" ,
                    horizontal_alignment= "center",
                )
            )
        page.update()
        
        
        
        
        
    def view_pop(view):
        page.views.pop()
        top_view=page.views[-1]
        page.go(top_view.route)
        
    page.on_route_change=route_change
    page.on_view_pop=view_pop
    page.window_width = 390
    page.window_height = 844
    page.window_maximizable=False
    
    page.go(page.route)
# Start the Wi-Fi status update in a separate thread
    start_wifi_status_update(page, wifi_status)
ft.app(target=main,view=WEB_BROWSER,
    assets_dir="assets")        