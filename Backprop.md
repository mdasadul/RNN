
## RNN
h(t) = tanh(Wxh*X+ Whh*h(t-1) +bh)
y = Wy*h(t) +by
Loss L = -log(exp(y)/sum(exp(y)))

let's consider Z = Wxh*X+ Whh*h(t-1) +bh
so h(t) = tanh(Z)

Also let's consider p = exp(y)/sum(exp(y)
so L = -log(p)
dL/dy = -(1/p)*dp/dy
      = -(1/p)* (sum(exp(y))*exp(y)-exp(y)*exp(y))/(sum(exp(y)))^2
      =-(1/p)(p-p^2)
      =p-1
      
dL/dWy =dL/dy*dy/dWy
       =(p-1)*h(t-1)
       
dL/dby =dL/dy*dy/dby
       =(p-1)*1 = p-1

dL/dh(t) = dL/dy*dy/d(h(t))
         = (p-1)*Wh + h_next
-----------------------------------------
dL/dZ = dL/dh(t)*dh(t)/dZ
      = ((p-1)*Wh + h_next) *(1-tanh^2(Z))
      = ((p-1)*Wh + h_next) *(1-h^2(t))
