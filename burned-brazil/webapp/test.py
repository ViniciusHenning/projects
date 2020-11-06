import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


x = np.linspace(0,1,100)
y = x**2

plt.plot(x, y)
plt.show()


