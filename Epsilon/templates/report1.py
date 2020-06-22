#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 11:36:37 2020

@author: juanis
"""


# Mover a administrador 
df = pd.DataFrame(students_class, columns =['user', 'student', 'class_name', 'grade1', 'grade2', 'grade3', 'grade4','grade5','grade_final'])
df["grupo_promedio"] = pd.cut(df['grade_final'], bins=[n * 0.5 for n in range(11)])
conteo_promedio = df['grupo_promedio'].groupby([df['grupo_promedio']]).count()
sns.set(font_scale=1.2)
ax = conteo_promedio.plot.bar(x="Promedio Final", y="Numero Estudiantes", rot=50, title="Promedio estudiantes materia")
ax.set(
    ylabel="Numero estudiantes",
    xlabel="Promedio Final",
    )
plt.savefig('Reporte.png')