class MetropolisHastings():
    def __init__(self, dataset):
        self.dataset = dataset
        self.N = dataset.size(0)

    def run(self, T, theta, data):
        S = torch.zeros(T, theta.size(0))
        S[0,:] = theta
        for i in range(T-1):
            S[i+1,:] = self.mh_step(S[i,:], data)
        return S

    def mh_step(self, theta, data):
        theta_new = self.get_theta_new(theta)
        log_alpha = self.get_log_alpha(theta, theta_new, data)
        log_u = torch.log(torch.rand(1))/ data.size(0)
        if log_u < log_alpha:
            theta = theta_new
        return theta

    def get_theta_new(self, theta):
        return theta + self.get_stepsize()*torch.randn(2)

    def get_log_alpha(self, theta, theta_new, data):
        lkhd = self.get_log_lkhd(theta_new, data) - self.get_log_lkhd(theta, data) # lkhd_new - lkhd_old
        return torch.mean(lkhd)

    def get_log_lkhd(self, theta, data):
        return -(((data - theta[0])/theta[1])**2)/2 - torch.log(theta[1]) # -((data-mu)/sig)**2 - log(sig)

    def get_stepsize(self):
        return 0.5/torch.sqrt(torch.tensor([self.N])) # 0.5/sqrt(N)