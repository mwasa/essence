from module import Module
import numpy as np

class Loss(Module):
    def __init__(self, _, pred_shape, truth_shape):
        self._out_shape = ()

    def forward(self, x, truth):
        self._t = truth
        return self._cal_loss(x)
    
    def backward(self, grad):
        return self._cal_grad(grad), None

class softmax_crossent(Loss):
    def _cal_loss(self, x):
        x -= x.max(1, keepdims = True)
        sum_e_x = np.exp(x).sum(1, keepdims = True)
        self._log_soft = x - np.log(sum_e_x)
        crossed = - np.multiply(self._t, self._log_soft)
        return crossed.sum(1).mean()

    def _cal_grad(self, grad):
        scalar = 1. / self._t.shape[0] * grad
        return scalar * (np.exp(self._log_soft) - self._t)

class crossent(Loss):
    def _cal_loss(self, x):
        self._x = x
        crossed = - np.multiply(self._t, np.log(x))
        return crossed.sum(1).mean() 

    def _cal_grad(self, grad):
        dLdp = - np.divide(self._t, self._x + 1e-20)
        return 1./self._batch * grad * dLdp

class l2(Loss):
    def _cal_loss(self, x):
        self._diff = x - self._t
        return np.pow(self._diff, 2).mean()

    def _cal_grad(self, grad):
        return grad * self._diff