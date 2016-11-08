#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
vimeval
imap <leader>l <C-k>*l
imap <leader>b <C-k>*b
imap <leader>F <C-k>*F
imap <leader>a <C-k>*a
endeval
"""

import numpy as np

e = np.e

α = 0.4
t = np.linspace(0, 1)
Φ = np.power(e, α*t)

print(Φ)
