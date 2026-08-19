import customtkinter as ctk
from bank import Bank
import datetime

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  

class BankGUI:
    def __init__(self, root, bank_system):
        self.root = root
        self.bank = bank_system
        
        self.root.title("سامانه مدیریت عملیات بانکی")
        self.root.geometry("850x550") 

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="پنل مدیریت بانک", font=("IRANSansX", 20, "bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=30)

        self.btn_dashboard = ctk.CTkButton(self.sidebar_frame, text="داشبورد", command=self.show_dashboard)
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=10)

        self.btn_customers = ctk.CTkButton(self.sidebar_frame, text="مدیریت مشتریان", command=self.show_customers)
        self.btn_customers.grid(row=2, column=0, padx=20, pady=10)

        self.btn_customer_list = ctk.CTkButton(self.sidebar_frame, text="لیست مشتریان و حساب‌ها", command=self.show_customer_list)
        self.btn_customer_list.grid(row=3, column=0, padx=20, pady=10)

        self.btn_transfer = ctk.CTkButton(self.sidebar_frame, text="انتقال وجه", command=self.show_transfer)
        self.btn_transfer.grid(row=4, column=0, padx=20, pady=10)

        self.btn_reports = ctk.CTkButton(self.sidebar_frame, text="گزارشات و لاگ‌ها", command=self.show_reports)
        self.btn_reports.grid(row=5, column=0, padx=20, pady=10)

        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.show_dashboard()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main_frame()
        
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(20, 10), padx=20)

        title = ctk.CTkLabel(header_frame, text="داشبورد مدیریت سیستم", font=("IRANSansX", 24, "bold"))
        title.pack(side="right")

        self.clock_label = ctk.CTkLabel(header_frame, text="", font=("IRANSansX", 14), text_color="#f1c40f")
        self.clock_label.pack(side="left", pady=5)
        self.update_clock() 

        stats_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=10, padx=20)
        
        card1 = ctk.CTkFrame(stats_frame, corner_radius=10, fg_color="#2c3e50")
        card1.pack(side="right", fill="both", expand=True, padx=5)
        ctk.CTkLabel(card1, text="تعداد کل مشتریان", font=("IRANSansX", 14)).pack(pady=(10, 0))
        self.lbl_total_customers = ctk.CTkLabel(card1, text="-", font=("IRANSansX", 24, "bold"))
        self.lbl_total_customers.pack(pady=(0, 10))

        card2 = ctk.CTkFrame(stats_frame, corner_radius=10, fg_color="#27ae60")
        card2.pack(side="right", fill="both", expand=True, padx=5)
        ctk.CTkLabel(card2, text="حساب‌های پس‌انداز", font=("IRANSansX", 14)).pack(pady=(10, 0))
        self.lbl_savings = ctk.CTkLabel(card2, text="-", font=("IRANSansX", 24, "bold"))
        self.lbl_savings.pack(pady=(0, 10))

        card3 = ctk.CTkFrame(stats_frame, corner_radius=10, fg_color="#c0392b")
        card3.pack(side="right", fill="both", expand=True, padx=5)
        ctk.CTkLabel(card3, text="حساب‌های جاری", font=("IRANSansX", 14)).pack(pady=(10, 0))
        self.lbl_checking = ctk.CTkLabel(card3, text="-", font=("IRANSansX", 24, "bold"))
        self.lbl_checking.pack(pady=(0, 10))

        quick_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        quick_frame.pack(fill="x", pady=10, padx=20)
        
        ctk.CTkLabel(quick_frame, text="دسترسی سریع", font=("IRANSansX", 14, "bold")).pack(side="right", padx=10)
        ctk.CTkButton(quick_frame, text="مشتری جدید", width=120, command=self.show_customers).pack(side="right", padx=5)
        ctk.CTkButton(quick_frame, text="انتقال وجه", width=120, command=self.show_transfer).pack(side="right", padx=5)

        events_frame = ctk.CTkFrame(self.main_frame)
        events_frame.pack(fill="both", expand=True, pady=10, padx=20)
        
        ctk.CTkLabel(events_frame, text="آخرین رویدادهای سیستم", font=("IRANSansX", 16, "bold")).pack(pady=(10, 5))
        
        self.events_textbox = ctk.CTkTextbox(events_frame, font=("IRANSansX", 12), height=120)
        self.events_textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.refresh_dashboard_data()

    def refresh_dashboard_data(self):
        if not hasattr(self, 'events_textbox') or not self.events_textbox.winfo_exists():
            return
        
        try:
            self.bank.load_data()
        except:
            pass

        total_customers = len(self.bank.customers)
        savings_count = sum(1 for acc in self.bank.accounts.values() if acc.__class__.__name__ == "SavingsAccount")
        checking_count = sum(1 for acc in self.bank.accounts.values() if acc.__class__.__name__ == "CheckingAccount")

        self.lbl_total_customers.configure(text=str(total_customers))
        self.lbl_savings.configure(text=str(savings_count))
        self.lbl_checking.configure(text=str(checking_count))

        self.events_textbox.configure(state="normal")
        self.events_textbox.delete("1.0", "end")
        try:
            with open('transactions.log', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                last_5_events = lines[-5:]
                if not last_5_events:
                    self.events_textbox.insert("1.0", "رویدادی ثبت نشده است.")
                else:
                    for line in reversed(last_5_events):
                        self.events_textbox.insert("end", line)
        except FileNotFoundError:
            self.events_textbox.insert("1.0", "فایل لاگ یافت نشد.")
            
        self.events_textbox.configure(state="disabled")

        self.root.after(2000, self.refresh_dashboard_data)

    def update_clock(self):
        try:
            now = datetime.datetime.now().strftime("%Y/%m/%d  %H:%M:%S")
            self.clock_label.configure(text=f"زمان: {now}")
            self.root.after(1000, self.update_clock)
        except:
            pass

    def show_customers(self):
        self.clear_main_frame()
        
        title1 = ctk.CTkLabel(self.main_frame, text="۱. ثبت مشتری جدید", font=("IRANSansX", 20, "bold"))
        title1.pack(pady=(20, 10))

        self.name_entry = ctk.CTkEntry(self.main_frame, placeholder_text="نام و نام خانوادگی", width=250, font=("IRANSansX", 14))
        self.name_entry.pack(pady=5)

        self.nid_entry = ctk.CTkEntry(self.main_frame, placeholder_text="کد ملی (۱۰ رقم)", width=250, font=("IRANSansX", 14))
        self.nid_entry.pack(pady=5)

        submit_btn = ctk.CTkButton(self.main_frame, text="ثبت مشتری", font=("IRANSansX", 14), command=self.register_customer)
        submit_btn.pack(pady=10)

        self.msg_label = ctk.CTkLabel(self.main_frame, text="", font=("IRANSansX", 14))
        self.msg_label.pack(pady=5)

        separator = ctk.CTkFrame(self.main_frame, height=2, fg_color="gray")
        separator.pack(fill="x", padx=40, pady=10)

        title2 = ctk.CTkLabel(self.main_frame, text="۲. افتتاح حساب بانکی", font=("IRANSansX", 20, "bold"))
        title2.pack(pady=(10, 10))

        self.acc_nid_entry = ctk.CTkEntry(self.main_frame, placeholder_text="کد ملی مشتری", width=250, font=("IRANSansX", 14))
        self.acc_nid_entry.pack(pady=5)

        self.acc_type_menu = ctk.CTkOptionMenu(
            self.main_frame, 
            values=["پس‌انداز (Savings)", "جاری (Checking)"], 
            width=250, 
            font=("IRANSansX", 14)
        )
        self.acc_type_menu.pack(pady=5)

        self.initial_balance_entry = ctk.CTkEntry(self.main_frame, placeholder_text="موجودی اولیه (تومان)", width=250, font=("IRANSansX", 14))
        self.initial_balance_entry.pack(pady=5)

        open_acc_btn = ctk.CTkButton(self.main_frame, text="افتتاح حساب", font=("IRANSansX", 14), command=self.create_account_gui)
        open_acc_btn.pack(pady=10)

        self.acc_msg_label = ctk.CTkLabel(self.main_frame, text="", font=("IRANSansX", 14))
        self.acc_msg_label.pack(pady=5)

    def register_customer(self):
        name = self.name_entry.get()
        nid = self.nid_entry.get()

        if not name or not nid:
            self.msg_label.configure(text="لطفاً همه فیلدها را پر کنید!", text_color="red")
            return

        try:
            self.bank.create_customer(name, nid)
            self.msg_label.configure(text=f"مشتری {name} با موفقیت ثبت شد.", text_color="green")
            self.name_entry.delete(0, 'end')
            self.nid_entry.delete(0, 'end')
            
            self.bank.save_data()
            
        except Exception as e:
            self.msg_label.configure(text=str(e), text_color="red")

    def create_account_gui(self):
        nid = self.acc_nid_entry.get()
        selected_type = self.acc_type_menu.get()
        balance_str = self.initial_balance_entry.get()

        if not nid or not balance_str:
            self.acc_msg_label.configure(text="لطفاً کد ملی و موجودی اولیه را وارد کنید!", text_color="red")
            return

        acc_type = "savings" if "پس‌انداز" in selected_type else "checking"

        try:
            initial_balance = float(balance_str)
            
            new_account = self.bank.open_account(nid, acc_type)
            
            if initial_balance > 0:
                new_account.deposit(initial_balance)
                
            success_msg = f"حساب با شماره {new_account.account_number} با موفقیت افتتاح شد."
            self.acc_msg_label.configure(text=success_msg, text_color="green")
            
            self.acc_nid_entry.delete(0, 'end')
            self.initial_balance_entry.delete(0, 'end')
            
            self.bank.save_data()
            
        except ValueError:
            self.acc_msg_label.configure(text="خطا: موجودی اولیه باید یک عدد معتبر باشد!", text_color="red")
        except Exception as e:
            self.acc_msg_label.configure(text=str(e), text_color="red")

    def show_customer_list(self):
        self.clear_main_frame()
        try:
            self.bank.load_data()
        except:
            pass

        title = ctk.CTkLabel(self.main_frame, text="لیست جامع مشتریان بانک", font=("IRANSansX", 24, "bold"))
        title.pack(pady=20)

        list_textbox = ctk.CTkTextbox(self.main_frame, width=650, height=350, font=("IRANSansX", 14))
        list_textbox.pack(pady=10)

        if not self.bank.customers:
            list_textbox.insert("1.0", "هیچ مشتری در سامانه ثبت نشده است.")
        else:
            for nid, customer in self.bank.customers.items():
                list_textbox.insert("end", f" نام: {customer.name} | کد ملی: {nid}\n")
                if not customer.accounts:
                    list_textbox.insert("end", "   └─ فاقد حساب بانکی\n")
                else:
                    for acc in customer.accounts:
                        list_textbox.insert("end", f"   └─ شماره حساب: {acc.account_number} | موجودی: {acc.get_balance()} تومان\n")
                list_textbox.insert("end", "─" * 60 + "\n")
        
        list_textbox.configure(state="disabled")

    def show_transfer(self):
        self.clear_main_frame()
        title = ctk.CTkLabel(self.main_frame, text="انتقال وجه بین حساب‌ها", font=("IRANSansX", 24, "bold"))
        title.pack(pady=30)

        self.src_acc_entry = ctk.CTkEntry(self.main_frame, placeholder_text="شماره حساب مبدأ", width=250, font=("IRANSansX", 14))
        self.src_acc_entry.pack(pady=10)

        self.dst_acc_entry = ctk.CTkEntry(self.main_frame, placeholder_text="شماره حساب مقصد", width=250, font=("IRANSansX", 14))
        self.dst_acc_entry.pack(pady=10)

        self.amount_entry = ctk.CTkEntry(self.main_frame, placeholder_text="مبلغ انتقال (تومان)", width=250, font=("IRANSansX", 14))
        self.amount_entry.pack(pady=10)

        transfer_btn = ctk.CTkButton(self.main_frame, text="انجام انتقال", font=("IRANSansX", 14), command=self.process_transfer)
        transfer_btn.pack(pady=20)

        self.transfer_msg_label = ctk.CTkLabel(self.main_frame, text="", font=("IRANSansX", 14))
        self.transfer_msg_label.pack(pady=10)

    def process_transfer(self):
        src = self.src_acc_entry.get().strip()  
        dst = self.dst_acc_entry.get().strip()
        amount_str = self.amount_entry.get().strip()

        if not src or not dst or not amount_str:
            self.transfer_msg_label.configure(text="لطفاً همه فیلدها را پر کنید!", text_color="red")
            return

        try:
            amount = float(amount_str) 
            
            self.bank.transfer_funds(src, dst, amount)
            self.transfer_msg_label.configure(text="انتقال وجه با موفقیت انجام شد.", text_color="green")
            
            self.src_acc_entry.delete(0, 'end')
            self.dst_acc_entry.delete(0, 'end')
            self.amount_entry.delete(0, 'end')
            
            self.bank.save_data() 
            
        except ValueError:
            self.transfer_msg_label.configure(text="مبلغ وارد شده معتبر نیست!", text_color="red")
        except Exception as e:
            self.transfer_msg_label.configure(text=str(e), text_color="red")

    def show_reports(self):
        self.clear_main_frame()
        title = ctk.CTkLabel(self.main_frame, text="لاگ تراکنش‌های سیستم", font=("IRANSansX", 24, "bold"))
        title.pack(pady=20)

        self.log_textbox = ctk.CTkTextbox(self.main_frame, width=600, height=300, font=("IRANSansX", 12))
        self.log_textbox.pack(pady=10)

        refresh_btn = ctk.CTkButton(self.main_frame, text="بروزرسانی گزارش", font=("IRANSansX", 14), command=self.load_logs)
        refresh_btn.pack(pady=10)

        self.load_logs() 

    def load_logs(self):
        self.log_textbox.configure(state="normal") 
        self.log_textbox.delete("1.0", "end") 
        
        try:
            with open('transactions.log', 'r', encoding='utf-8') as file:
                logs = file.read()
                if logs.strip() == "":
                    self.log_textbox.insert("1.0", "هیچ تراکنشی  ثبت نشده است.")
                else:
                    self.log_textbox.insert("1.0", logs)
        except FileNotFoundError:
            self.log_textbox.insert("1.0", " (سیستم فاقد تراکنش است).")
            
        self.log_textbox.configure(state="disabled") 

if __name__ == "__main__":
    my_bank = Bank()
    my_bank.load_data()
    my_bank.start_interest_task()
    app = ctk.CTk()
    gui = BankGUI(app, my_bank)
    app.mainloop()