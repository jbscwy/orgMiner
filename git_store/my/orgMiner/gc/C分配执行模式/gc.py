class GC:
    # 种群的设计
    # 参数：资源日志、资源组执行模式矩阵、
    def __init__(self,
                 rl_file,   # 资源日志文件
                 initialize_populations, # 初始化种群
                 ogs, # 资源分组结果
                 execution_mode_group, # 执行模式组
                 modify_weight_metrix, # 执行模式权重矩阵
                 rl, # 资源日志
                 labels, # 资源分组标记
                 resource_matrix, # 资源执行模式矩阵
                 res,
                 crossover_probability,
                 mutation_probability,
                 mutation_num,
                 gen_max):

        self.individuals = initialize_populations # 种群
        self.size = len(initialize_populations)  # 种群所包含的个体数

        self.rl_file=rl_file

        self.labels=labels
        self.resource_matrix=resource_matrix

        self.res=res


        self.selector_probability=[] # 种群选择器

        self.new_individuals = initialize_populations   # 新一代个体集合

        self.first_fit_pre_f1=[0,0,0]

        self.ogs=ogs # 资源分组
        self.execution_mode_group=execution_mode_group # 执行模式组
        self.rl=rl # 资源日志

        self.crossover_probability = crossover_probability  # 个体之间的交叉概率
        self.mutation_probability = mutation_probability  # 个体之间的变异概率
        self.mutation_num=mutation_num

        self.generation_max = gen_max  # 种群进化的最大世代数
        self.age = 0  # 种群当前所处世代

        self.best_individual=0     # 保留最佳精英个体
        self.best_fit_pre_f1=[0,0,0] # 保留最佳精英个体最好的评估结果

        self.fit_pre_f1=[]

        self.modify_weight_metrix=modify_weight_metrix # 执行模式权重

        for i in range(len(initialize_populations)):
            self.selector_probability.append(0)
            self.fit_pre_f1.append([0,0,0])


    def _f1(self,fit, pre):
        n = fit * pre
        m = fit + pre
        if m != m:
            return 0.00000001
        return n / m

    # 生成组织模型
    def get_om_by_rem(self,individual):
        from orgminer.OrganizationalModelMiner.base import OrganizationalModel
        om = OrganizationalModel()
        for i in range(len(self.ogs)):
            modes = []
            for j in range(len(individual[0])):
                if individual[i][j] > 0:
                    modes.append(self.execution_mode_group[j])
            om.add_group(self.ogs[i], sorted(list(modes)))
        return om

    # 适应度函数
    def fitness_func(self,individual):
        from orgminer.Evaluation.l2m import conformance
        om=self.get_om_by_rem(individual)
        # 评估组织模型
        fitness_score = conformance.fitness(self.rl, om)
        precision_score = conformance.precision(self.rl, om)
        f1 = self._f1(fitness_score, precision_score) * 2
        return fitness_score, precision_score, f1

    # 用于评估种群中的个体集合 self.individuals 中各个个体的适应度
    def evaluate(self):
        sp = self.selector_probability
        best_fpf=[0,0,0]
        best_i=0
        worst_fpf = [1, 1, 1]
        worst_i=0
        for i in range(len(self.individuals)):
            fit,pre,f1=self.fitness_func(self.individuals[i])
            self.fit_pre_f1[i][0]=fit
            self.fit_pre_f1[i][1]=pre
            self.fit_pre_f1[i][2]=f1
            if self.fit_pre_f1[i][2]>best_fpf[2]:
                best_fpf[0]=fit
                best_fpf[1] = pre
                best_fpf[2] = f1
                best_i=i
            if self.fit_pre_f1[i][2]<worst_fpf[2]:
                worst_fpf[0]=fit
                worst_fpf[1] = pre
                worst_fpf[2] = f1
                worst_i=i
        self.res.append([self.rl_file,best_fpf[0],best_fpf[1],best_fpf[2]])
        print("当前迭代最好结果，fit:" + str(self.best_fit_pre_f1[0]) + ",pre:" + str(self.best_fit_pre_f1[1]) + ",f1:" + str(
            self.best_fit_pre_f1[2]))
        if best_fpf[2]>=self.best_fit_pre_f1[2]:
            self.best_fit_pre_f1[0]=best_fpf[0]
            self.best_fit_pre_f1[1]=best_fpf[1]
            self.best_fit_pre_f1[2]=best_fpf[2]
            self.best_individual=self.individuals[best_i]
        else:
            self.individuals[worst_i]=self.best_individual
        print("历史最好结果，fit:" + str(self.best_fit_pre_f1[0]) + ",pre:" + str(self.best_fit_pre_f1[1]) + ",f1:" + str(self.best_fit_pre_f1[2]))
        ft_sum = float(0)
        for i in range(len(self.fit_pre_f1)):
            ft_sum += self.fit_pre_f1[i][2]
        for j in range(self.size):
            sp[j] = self.fit_pre_f1[j][2] / float(ft_sum)  # 得到各个个体的生存概率
        for k in range(1, self.size):
            sp[k] = sp[k] + sp[k - 1]  # 需要将个体的生存概率进行叠加，从而计算出各个个体的选择概率


    # 选择算子,轮盘选择
    def select(self):
        import random
        t=random.random()
        for i in range(len(self.selector_probability)):
            if t<=self.selector_probability[i]:
                return i
        return self.size-1


    # 交叉算子
    def crossover(self,i, j):

        import random
        p = random.random()  # 随机概率
        father = self.individuals[i]
        mather = self.individuals[j]
        if i != j and p < self.crossover_probability:
            l = len(father)
            d1 = []
            # 如何切分两个矩阵
            for i in range(l):
                import random
                t2 = random.random()
                if t2 > 0.5:
                    d1.append(i)
            # print(d1)
            child = []
            for j in range(l):
                if j in d1:
                    child.append(father[j])
                else:
                    child.append(mather[j])
            return child
        else:
            return father



    # 变异算子
    def mutate(self,individual):
        import random
        p = random.random()
        if p < self.mutation_probability:
            for i in range(self.mutation_num):
                import copy
                indiv = copy.deepcopy(individual)
                t1 = random.randint(0, len(indiv) - 1)
                t2 = random.random()
                for j in range(len(indiv[0])):
                    if self.modify_weight_metrix[t1][j] != 0 and self.modify_weight_metrix[t1][j] > t2:
                        if indiv[t1][j] == 1:
                            indiv[t1][j] = 0
                        elif indiv[t1][j] == 0:
                            indiv[t1][j] = 1
                        break
            return indiv
        else:
            return individual


    # 进化过程
    def evolve(self):
        indivs = self.individuals
        new_indivs =[]
        # 计算适应度及选择概率
        self.evaluate()
        for i in range(len(indivs)):
            # print("选择")
            j=self.select()
            # 交叉
            # print("交叉")
            child=self.crossover(i, j)
            # 变异
            # print("变异")
            child=self.mutate(child)
            new_indivs.append(child)
        # 更新种群
        self.individuals=new_indivs


    # 运行主函数
    def run(self):
        for i in range(self.generation_max):
            print("第"+str(i)+"次迭代：")
            self.evolve()
            if i==0:
                self.first_fit_pre_f1=self.best_fit_pre_f1