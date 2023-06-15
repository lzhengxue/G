import tkinter as tk
import random
import copy

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.mains = {'暴击':1.555, '暴伤': 3.1, '精通':9.33, '充能':2.6, '大攻击':2.333, '大防御':2.9, '大生命':2.333, '小攻击':15.56, '小生命':239, 
                      '治疗':1.797,'火伤':2.333, '水伤':2.333, '雷伤':2.333, '冰伤':2.333, '草伤':2.333, '风伤':2.333, '岩伤':2.333, '物伤':2.9}
        self.subs = {'暴击':0.389, '暴伤':0.777, '精通':2.331, '充能':0.648, '大攻击':0.583, '大防御':0.729, '大生命':0.583, '小攻击':1.945, '小生命':29.875, '小防御':2.315}
        self.enhance_flag = -1
        self.possible_stats = ['暴击', '暴伤', '精通', '充能', '大攻击', '大防御', '大生命', '小攻击', '小生命', '小防御']
        self.main_stat = None
        self.main_stat_value = 0
        self.sub_stats = []
        self.sub_stat_values = []
        self.equipment_type = None
        self.types = ["生之花", "死之羽", "时之沙", "空之杯", "理之冠"]


        self.initialize = tk.Button(self)
        self.initialize["text"] = "初始化装备"
        self.initialize["command"] = self.initialize_equipment
        self.initialize.pack(side="top")

        self.enhance = tk.Button(self)
        self.enhance["text"] = "强化装备"
        self.enhance["command"] = self.enhance_equipment
        self.enhance.pack(side="top")

        self.reset = tk.Button(self)
        self.reset["text"] = "重置装备"
        self.reset["command"] = self.reset_equipment
        self.reset.pack(side="top")

        self.output = tk.Text(self, height=10, width=50)
        self.output.pack(side="bottom")

    def initialize_equipment(self):
        self.enhance_flag = 0
        self.possible_stats = ['暴击', '暴伤', '精通', '充能', '大攻击', '大防御', '大生命', '小攻击', '小生命', '小防御']
        self.main_stat = None
        self.sub_stats = []
        self.sub_stat_values = []
        self.equipment_type = None
        self.types = ["生之花", "死之羽", "时之沙", "空之杯", "理之冠"]

        self.equipment_type = random.choice(self.types)

        if self.equipment_type == "生之花":
            self.main_stat = "小生命"
        elif self.equipment_type == "死之羽":
            self.main_stat = "小攻击"
        elif self.equipment_type == "时之沙":
            items_shalou = ['精通', '充能', '大攻击', '大防御', '大生命']
            weights_shalou = [3, 3, 8, 8, 8]
            sum1 = sum(weights_shalou)
            choice = random.uniform(0, sum1)
            for i in range(len(weights_shalou)):
                choice -= weights_shalou[i]
                if choice <= 0:
                    self.main_stat = items_shalou[i]
                    break
        elif self.equipment_type == "空之杯":
            items_beizi = ['大攻击', '大防御', '大生命', '属伤', '精通']
            weights_beizi = [19.175, 19.15, 19.175, 40, 2.5]
            sum1 = sum(weights_beizi)
            
            choice = random.uniform(0, sum1)
            for i in range(len(weights_beizi)):
                choice -= weights_beizi[i]
                if choice <= 0:
                    self.main_stat = items_beizi[i]
                    if self.main_stat == '属伤':
                        self.main_stat = random.choice(['火伤', '水伤', '雷伤', '冰伤', '草伤', '风伤', '岩伤', '物伤'])
                    break
        elif self.equipment_type == "理之冠":
            items_tou = ['大攻击', '大防御', '大生命', '暴击', '暴伤', '治疗', '精通']
            weights_tou = [11, 11, 11, 5, 5, 5, 2]
            sum1 = sum(weights_tou)
            choice = random.uniform(0, sum1)
            for i in range(len(weights_tou)):
                choice -= weights_tou[i]
                if choice <= 0:
                    self.main_stat = items_tou[i]
                    break

        self.possible_sub_stats = [stat for stat in self.possible_stats if stat != self.main_stat]
        self.possible_sub_stats_weight = [3, 3, 4, 4, 4, 4, 4, 6, 6, 6]
        if self.main_stat in '暴击暴伤':self.possible_sub_stats_weight.remove(3)
        elif self.main_stat in '精通充能大攻击大防御大生命':self.possible_sub_stats_weight.remove(4)
        elif self.main_stat in '小攻击小生命小防御':self.possible_sub_stats_weight.remove(6)

        num_of_sub_stats = random.choice([3, 3, 3, 3, 4])
        for i in range(num_of_sub_stats):
            sum2 = sum(self.possible_sub_stats_weight)
            choice = random.uniform(0, sum2)
            for j in range(len(self.possible_sub_stats_weight)):
                choice -= self.possible_sub_stats_weight[j]
                if choice <= 0:
                    self.sub_stats.append(self.possible_sub_stats[j])
                    self.sub_stat_values.append(random.choice([7, 8, 9, 10]))
                    self.possible_sub_stats.remove(self.possible_sub_stats[j])
                    self.possible_sub_stats_weight.remove(self.possible_sub_stats_weight[j])
                    break

        self.main_stat_value = 3

        m = copy.deepcopy(self.main_stat)
        mv = copy.deepcopy(self.main_stat_value)
        s = copy.deepcopy(self.sub_stats)
        sv = copy.deepcopy(self.sub_stat_values)
        et = copy.deepcopy(self.equipment_type)
    
    
        self.initial_values = {
            "main_stat": m, 
            "main_stat_value": mv,
            "sub_stats": s, 
            "sub_stat_values": sv,
            "equipment_type": et
        }
        self.update_equipment_status()

    def enhance_equipment(self):
        if self.enhance_flag < 5 and self.enhance_flag >=0 :
            self.main_stat_value += 3.4
            if len(self.sub_stats) == 3:
                sum2 = sum(self.possible_sub_stats_weight)
                choice = random.uniform(0, sum2)
                for j in range(len(self.possible_sub_stats_weight)):
                    choice -= self.possible_sub_stats_weight[j]
                    if choice <= 0:
                        self.sub_stats.append(self.possible_sub_stats[j])
                        self.sub_stat_values.append(random.choice([7, 8, 9, 10]))
                        break
            elif len(self.sub_stats) == 4:
                chosen_sub_stat = random.choice(range(4))
                self.sub_stat_values[chosen_sub_stat] += random.choice([7, 8, 9, 10])
            self.enhance_flag += 1
        self.update_equipment_status()

    def reset_equipment(self):
        if self.enhance_flag == -1:
            self.update_equipment_status()
        else:
            self.enhance_flag = 0
            self.main_stat = self.initial_values["main_stat"]
            self.main_stat_value = self.initial_values["main_stat_value"]
            self.sub_stats = copy.deepcopy(self.initial_values["sub_stats"])
            self.sub_stat_values = copy.deepcopy(self.initial_values["sub_stat_values"])
            self.equipment_type = self.initial_values["equipment_type"]
            self.update_equipment_status()
    

    def update_equipment_status(self):
        self.output.delete(1.0, tk.END)
        if self.enhance_flag == -1:
            self.output.insert(tk.END, f"尚未初始化装备")

        if self.main_stat and self.sub_stats and self.equipment_type and self.enhance_flag != -1:
            self.output.insert(tk.END, f"装备类型: {self.equipment_type}\n")
            self.output.insert(tk.END, f"主词条: {self.main_stat} {self.main_stat_value*(self.mains[self.main_stat])}\n")
            for i in range(len(self.sub_stats)):
                self.output.insert(tk.END, f"副词条{i+1}: {self.sub_stats[i]} {self.sub_stat_values[i]*(self.subs[self.sub_stats[i]])}\n")
            if self.enhance_flag>4:
                self.output.insert(tk.END, f"已达强化次数上限")

        else:
            self.output.insert(tk.END, "请先初始化装备\n")

root = tk.Tk()
root.title('圣遗物强化模拟器v1')
app = Application(master=root)
app.mainloop()
