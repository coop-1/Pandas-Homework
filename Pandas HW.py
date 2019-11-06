#!/usr/bin/env python
# coding: utf-8

# In[179]:


import pandas as pd
import os

#macOS pathing format
schools = "/Users/crobinson1205/LearnPython/PyCitySchools_schools.csv"
students = "/Users/crobinson1205/LearnPython/PyCitySchools_students.csv"
#windows pathing format
#schools= r"H:\TempPython\PyCitySchools_schools.csv"
#students = r"H:\TempPython\PyCitySchools_students.csv"

#read in raw data
schools_df = pd.read_csv(schools)
students_df = pd.read_csv(students)

#add grade bins to students original table
grade_bin = [0,69,100]
grade_names = ["Fail","Pass"]

students_df["Pass/Fail_math"] = pd.cut(students_df["math_score"], grade_bin, labels=grade_names)
students_df["Pass/Fail_reading"] = pd.cut(students_df["reading_score"], grade_bin, labels=grade_names)

#add budget per student to schools original table
schools_df["budget_per_student"] = schools_df["budget"]/schools_df["size"]
#print(schools_df)

#size by district table
district_size = schools_df.groupby("type", as_index=False)["size"].sum()

#merge of the two original CSV's
school_data_complete = pd.merge(students_df, schools_df, how = "left", on = ["school_name", "school_name"])

schools_df["TotalAgg"] = "Combined"
students_df["TotalAgg"] = "Combined"


# In[180]:


#TOTAL AGG TABLE - EVERYTHING SUMMARIZED

#get total schools
totalagg_schools = schools_df.groupby("TotalAgg", as_index=False)["school_name"].count()

#get total size
totalagg_size = schools_df.groupby("TotalAgg", as_index=False)["size"].sum()

#get total budget
totalagg_budget = schools_df.groupby("TotalAgg", as_index=False)["budget"].sum()

#get total students who passed math
totalagg_passmath = students_df[students_df["Pass/Fail_math"] == "Pass"].groupby("TotalAgg", as_index=False).count()
totalagg_passmath = totalagg_passmath.rename(columns = {"Student ID":"Students_Passed_Math"})

#get total students who passed reading
totalagg_passreading = students_df[students_df["Pass/Fail_reading"] == "Pass"].groupby("TotalAgg", as_index=False).count()
totalagg_passreading = totalagg_passreading.rename(columns = {"Student ID":"Students_Passed_Reading"})

#BUILDING SUMMARY TABLE
totalaggsummary = pd.merge(totalagg_schools,totalagg_size,how="left", on = ["TotalAgg","TotalAgg"])
totalaggsummary = pd.merge(totalaggsummary,totalagg_budget,how="left", on = ["TotalAgg","TotalAgg"])
totalaggsummary = pd.merge(totalaggsummary,totalagg_passmath[["TotalAgg","Students_Passed_Math"]],how="left", on = "TotalAgg")
totalaggsummary = pd.merge(totalaggsummary,totalagg_passreading[["TotalAgg","Students_Passed_Reading"]],how="left", on = "TotalAgg")

totalaggsummary["Students_Passed_Math(%)"] = totalaggsummary["Students_Passed_Math"]/totalaggsummary["size"]
totalaggsummary["Students_Passed_Reading(%)"] = totalaggsummary["Students_Passed_Reading"]/totalaggsummary["size"]
totalaggsummary["Overall_Passing_Rate"] = (totalaggsummary["Students_Passed_Reading"]+totalaggsummary["Students_Passed_Math"])/(totalaggsummary["size"]*2)

totalaggsummary.rename(columns = {'Overall_Passing_Rate':'Overall Passing Rate'}, inplace = True)
totalaggsummary.rename(columns = {'Students_Passed_Math(%)':'Students Passed Math (%)'}, inplace = True)
totalaggsummary.rename(columns = {'Students_Passed_Reading(%)':'Students Passed Reading (%)'}, inplace = True)
totalaggsummary.rename(columns = {'Students_Passed_Reading':'Students Passed Reading (Total)'}, inplace = True)
totalaggsummary.rename(columns = {'Students_Passed_Math':'Students Passed Math (Total)'}, inplace = True)
totalaggsummary.rename(columns = {'size':'Total Students'}, inplace = True)
totalaggsummary.rename(columns = {'school_name':'Total Schools'}, inplace = True)
totalaggsummary.rename(columns = {'budget':'Total Budget'}, inplace = True)

totalaggsummary.style.format({
    'Overall Passing Rate': '{:,.2%}'.format,
    'Students Passed Math (%)': '{:,.2%}'.format,
    'Students Passed Reading (%)': '{:,.2%}'.format,
    'Total Students': '{:,.0f}'.format,
    'Total Budget': '${:,.0f}'.format,
    'Students Passed Math (Total)': '{:,.0f}'.format,
    'Students Passed Reading (Total)': '{:,.0f}'.format,
    'Total Schools': '{:,.0f}'.format,
})


# In[181]:


#SCHOOL SUMMARY

#avg math agg table by school NAME
avgmath_name = school_data_complete.groupby("school_name", as_index=False)["math_score"].mean()

#avg math agg table by school TYPE
avgmath_type = school_data_complete.groupby("type", as_index=False)["math_score"].mean()

#avg reading agg table by school NAME
avgreading_name = school_data_complete.groupby("school_name", as_index=False)["reading_score"].mean()

#avg reading agg table by school TYPE
avgreading_type = school_data_complete.groupby("type", as_index=False)["reading_score"].mean()

#adding updated schools_df to students_df - could replace all students_df going forward to make code cleaner
students_df = pd.merge(students_df,schools_df,how="left", on = ["school_name","school_name"])

#number of students that pass math table by school NAME
totalpassmath_name = students_df[students_df["Pass/Fail_math"] == "Pass"].groupby("school_name", as_index=False).count()
totalpassmath_name = totalpassmath_name.rename(columns = {"Student ID":"Students_Passed_Math"})

#number of students that pass math table by school TYPE
totalpassmath_type = students_df[students_df["Pass/Fail_math"] == "Pass"].groupby("type", as_index=False).count()
totalpassmath_type = totalpassmath_type.rename(columns = {"Student ID":"Students_Passed_Math"})

##number of students that pass reading table by school NAME
totalpassreading_name = students_df[students_df["Pass/Fail_reading"] == "Pass"].groupby("school_name", as_index=False).count()
totalpassreading_name = totalpassreading_name.rename(columns = {"Student ID":"Students_Passed_Reading"})

#number of students that pass reading table by school TYPE
totalpassreading_type = students_df[students_df["Pass/Fail_reading"] == "Pass"].groupby("type", as_index=False).count()
totalpassreading_type = totalpassreading_type.rename(columns = {"Student ID":"Students_Passed_Reading"})

#BUILDING FINAL TABLE
schoolsummary = pd.merge(schools_df , avgmath_name,how="left", on = ["school_name","school_name"])
schoolsummary = pd.merge(schoolsummary , avgreading_name,how="left", on = ["school_name","school_name"])
schoolsummary = pd.merge(schoolsummary,totalpassmath_name[["school_name","Students_Passed_Math"]],how="left", on = "school_name")
schoolsummary = pd.merge(schoolsummary,totalpassreading_name[["school_name","Students_Passed_Reading"]],how="left", on = "school_name")
schoolsummary["Students_Passed_Math(%)"] = schoolsummary["Students_Passed_Math"]/schoolsummary["size"]
schoolsummary["Students_Passed_Reading(%)"] = schoolsummary["Students_Passed_Reading"]/schoolsummary["size"]
schoolsummary["Overall_Passing_Rate"] = (schoolsummary["Students_Passed_Reading"]+schoolsummary["Students_Passed_Math"])/(schoolsummary["size"]*2)

del schoolsummary["School ID"]
del schoolsummary["TotalAgg"]

schoolsummary.rename(columns = {'school_name':'School Name'}, inplace = True)
schoolsummary.rename(columns = {'type':'School Type'}, inplace = True)
schoolsummary.rename(columns = {'size':'Total Students'}, inplace = True)
schoolsummary.rename(columns = {'budget':'Budget (Total)'}, inplace = True)
schoolsummary.rename(columns = {'budget_per_student':'Budget (Per Student)'}, inplace = True)
schoolsummary.rename(columns = {'math_score':'Average Math Score'}, inplace = True)
schoolsummary.rename(columns = {'reading_score':'Average Reading Score'}, inplace = True)
schoolsummary.rename(columns = {'Students_Passed_Math':'Students Passed Math (Total)'}, inplace = True)
schoolsummary.rename(columns = {'Students_Passed_Reading':'Students Passed Reading (Total)'}, inplace = True)
schoolsummary.rename(columns = {'Students_Passed_Math(%)':'Students Passed Math (%)'}, inplace = True)
schoolsummary.rename(columns = {'Students_Passed_Reading(%)':'Students Passed Reading (%)'}, inplace = True)
schoolsummary.rename(columns = {'Overall_Passing_Rate':'Overall Passing Rate'}, inplace = True)

schoolsummary.style.format({
    'Overall Passing Rate': '{:,.2%}'.format,
    'Students Passed Math (%)': '{:,.2%}'.format,
    'Students Passed Reading (%)': '{:,.2%}'.format,
    'Total Students': '{:,.0f}'.format,
    'Budget (Total)': '${:,.0f}'.format,
    'Students Passed Math (Total)': '{:,.0f}'.format,
    'Students Passed Reading (Total)': '{:,.0f}'.format,
    'Total Schools': '{:,.0f}'.format,
})


# In[182]:


#SCHOOL SUMMARY by top 5 highest performing
schoolsummaryhighest = schoolsummary.sort_values(by='Overall Passing Rate',ascending=False)
schoolsummaryhighest.head().style.format({
    'Overall Passing Rate': '{:,.2%}'.format,
    'Students Passed Math (%)': '{:,.2%}'.format,
    'Students Passed Reading (%)': '{:,.2%}'.format,
    'Total Students': '{:,.0f}'.format,
    'Budget (Total)': '${:,.0f}'.format,
    'Students Passed Math (Total)': '{:,.0f}'.format,
    'Students Passed Reading (Total)': '{:,.0f}'.format,
    'Total Schools': '{:,.0f}'.format,
})


# In[183]:


#SCHOOL SUMMARY by top 5 worst performing
schoolsummarylowest = schoolsummary.sort_values(by='Overall Passing Rate',ascending=True)
schoolsummarylowest.head().style.format({
    'Overall Passing Rate': '{:,.2%}'.format,
    'Students Passed Math (%)': '{:,.2%}'.format,
    'Students Passed Reading (%)': '{:,.2%}'.format,
    'Total Students': '{:,.0f}'.format,
    'Budget (Total)': '${:,.0f}'.format,
    'Students Passed Math (Total)': '{:,.0f}'.format,
    'Students Passed Reading (Total)': '{:,.0f}'.format,
    'Total Schools': '{:,.0f}'.format,
})


# In[184]:


#TYPE SUMMARY

schooltypesummary = pd.merge(avgmath_type,avgreading_type,how="left", on = ["type","type"])
schooltypesummary = pd.merge(schooltypesummary,totalpassmath_type[["type","Students_Passed_Math"]],how="left", on = "type")
schooltypesummary = pd.merge(schooltypesummary,totalpassreading_type[["type","Students_Passed_Reading"]],how="left", on = "type")
schooltypesummary = pd.merge(schooltypesummary,district_size,how="left", on = ["type","type"])
schooltypesummary["Students_Passed_Math(%)"] = schooltypesummary["Students_Passed_Math"]/schooltypesummary["size"]
schooltypesummary["Students_Passed_Reading(%)"] = schooltypesummary["Students_Passed_Reading"]/schooltypesummary["size"]
schooltypesummary["Overall_Passing_Rate"] = (schooltypesummary["Students_Passed_Reading"]+schooltypesummary["Students_Passed_Math"])/(schooltypesummary["size"]*2)

schooltypesummary.rename(columns = {'school_name':'School Name'}, inplace = True)
schooltypesummary.rename(columns = {'type':'School Type'}, inplace = True)
schooltypesummary.rename(columns = {'size':'Total Students'}, inplace = True)
schooltypesummary.rename(columns = {'budget':'Budget (Total)'}, inplace = True)
schooltypesummary.rename(columns = {'budget_per_student':'Budget (Per Student)'}, inplace = True)
schooltypesummary.rename(columns = {'math_score':'Average Math Score'}, inplace = True)
schooltypesummary.rename(columns = {'reading_score':'Average Reading Score'}, inplace = True)
schooltypesummary.rename(columns = {'Students_Passed_Math':'Students Passed Math (Total)'}, inplace = True)
schooltypesummary.rename(columns = {'Students_Passed_Reading':'Students Passed Reading (Total)'}, inplace = True)
schooltypesummary.rename(columns = {'Students_Passed_Math(%)':'Students Passed Math (%)'}, inplace = True)
schooltypesummary.rename(columns = {'Students_Passed_Reading(%)':'Students Passed Reading (%)'}, inplace = True)
schooltypesummary.rename(columns = {'Overall_Passing_Rate':'Overall Passing Rate'}, inplace = True)

schooltypesummary.style.format({
    'Overall Passing Rate': '{:,.2%}'.format,
    'Students Passed Math (%)': '{:,.2%}'.format,
    'Students Passed Reading (%)': '{:,.2%}'.format,
    'Total Students': '{:,.0f}'.format,
    'Budget (Total)': '${:,.0f}'.format,
    'Students Passed Math (Total)': '{:,.0f}'.format,
    'Students Passed Reading (Total)': '{:,.0f}'.format,
    'Total Schools': '{:,.0f}'.format,
})


# In[185]:


#SCORE BREAKDOWN BY GRADE

#9TH GRADE 

    #9th grade filter table
ninthgrade = students_df[(students_df['grade'] == "9th")]

    #9th grade table grouped by high school - mean of math scores
ninthgrade_math = ninthgrade.groupby("school_name", as_index=False)["math_score"].mean()
ninthgrade_math = ninthgrade_math.rename(columns = {"math_score":"9th"})

    #9th grade table grouped by high school - mean of reading scores
ninthgrade_reading = ninthgrade.groupby("school_name", as_index=False)["reading_score"].mean()
ninthgrade_reading = ninthgrade_reading.rename(columns = {"reading_score":"9th"})

#10TH GRADE 

    #10th grade filter table
tenthgrade = students_df[(students_df['grade'] == "10th")]

    #10TH grade table grouped by high school - mean of math scores
tenthgrade_math = tenthgrade.groupby("school_name", as_index=False)["math_score"].mean()
tenthgrade_math = tenthgrade_math.rename(columns = {"math_score":"10th"})

    #10th grade table grouped by high school - mean of reading scores
tenthgrade_reading = tenthgrade.groupby("school_name", as_index=False)["reading_score"].mean()
tenthgrade_reading = tenthgrade_reading.rename(columns = {"reading_score":"10th"})

#11TH GRADE 

    #11th grade filter table
eleventhgrade = students_df[(students_df['grade'] == "11th")]

    #11TH grade table grouped by high school - mean of math scores
eleventhgrade_math = eleventhgrade.groupby("school_name", as_index=False)["math_score"].mean()
eleventhgrade_math = eleventhgrade_math.rename(columns = {"math_score":"11th"})

    #11TH grade table grouped by high school - mean of reading scores
eleventhgrade_reading = eleventhgrade.groupby("school_name", as_index=False)["reading_score"].mean()
eleventhgrade_reading = eleventhgrade_reading.rename(columns = {"reading_score":"11th"})

#12TH GRADE 

    #12TH grade filter table
twelfthgrade = students_df[(students_df['grade'] == "12th")]

    #12TH grade table grouped by high school - mean of math scores
twelfthgrade_math = twelfthgrade.groupby("school_name", as_index=False)["math_score"].mean()
twelfthgrade_math = twelfthgrade_math.rename(columns = {"math_score":"12th"})

    #12TH grade table grouped by high school - mean of reading scores
twelfthgrade_reading = twelfthgrade.groupby("school_name", as_index=False)["reading_score"].mean()
twelfthgrade_reading = twelfthgrade_reading.rename(columns = {"reading_score":"12th"})

#MATH SUMMARY TABLE by high school
mathsummary = pd.merge(ninthgrade_math,tenthgrade_math,how="left", on = ["school_name","school_name"])
mathsummary = pd.merge(mathsummary,eleventhgrade_math,how="left", on = ["school_name","school_name"])
mathsummary = pd.merge(mathsummary,twelfthgrade_math,how="left", on = ["school_name","school_name"])

mathsummary.rename(columns = {'school_name':'School Name'}, inplace = True)

mathsummary


# In[186]:


#READING SUMMARY TABLE by high school
readingsummary = pd.merge(ninthgrade_reading,tenthgrade_reading,how="left", on = ["school_name","school_name"])
readingsummary = pd.merge(readingsummary,eleventhgrade_reading,how="left", on = ["school_name","school_name"])
readingsummary = pd.merge(readingsummary,twelfthgrade_reading,how="left", on = ["school_name","school_name"])

readingsummary.rename(columns = {'school_name':'School Name'}, inplace = True)

readingsummary


# In[187]:


#SCORES BY SCHOOL SPENDING

#add in spending by student by school bands students table
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]

students_df["Spending Ranges (Per Student)"] = pd.cut(students_df["budget_per_student"], spending_bins, labels=group_names)

#get count of students for spend binds
countstudents_spendbin = students_df.groupby("Spending Ranges (Per Student)", as_index=False)["size"].count()

#gets average of math scores for spend bins
avgmath_spendbin = students_df.groupby("Spending Ranges (Per Student)", as_index=False)["math_score"].mean()

#gets average of reading scores for spend bins
avgreading_spendbin = students_df.groupby("Spending Ranges (Per Student)", as_index=False)["reading_score"].mean()

#counts number of students who passed math for spend bins
countmath_spendbin = students_df[students_df["Pass/Fail_math"] == "Pass"].groupby("Spending Ranges (Per Student)", as_index=False).count()
countmath_spendbin = countmath_spendbin.rename(columns = {"Student ID":"Students_Passed_Math"})

#counts number of students who passed reading for spend bins
countreading_spendbin = students_df[students_df["Pass/Fail_reading"] == "Pass"].groupby("Spending Ranges (Per Student)", as_index=False).count()
countreading_spendbin = countreading_spendbin.rename(columns = {"Student ID":"Students_Passed_Reading"})

#merge average reading and math scores to create summary table
schoolspending = pd.merge(avgmath_spendbin,avgreading_spendbin,how="left", on = ["Spending Ranges (Per Student)","Spending Ranges (Per Student)"])

#add count of students that passed math to summary table
schoolspending = pd.merge(schoolspending,countmath_spendbin[["Spending Ranges (Per Student)","Students_Passed_Math"]],how="left", on = ["Spending Ranges (Per Student)","Spending Ranges (Per Student)"])

#add count of students that passed reading to summary table
schoolspending = pd.merge(schoolspending,countreading_spendbin[["Spending Ranges (Per Student)","Students_Passed_Reading"]],how="left", on = ["Spending Ranges (Per Student)","Spending Ranges (Per Student)"])

#add school size to summary table
schoolspending = pd.merge(countstudents_spendbin,schoolspending,how="left", on = ["Spending Ranges (Per Student)","Spending Ranges (Per Student)"])

#% students that passed
schoolspending["Students_Passed_Math(%)"] = schoolspending["Students_Passed_Math"]/schoolspending["size"]
schoolspending["Students_Passed_Reading(%)"] = schoolspending["Students_Passed_Reading"]/schoolspending["size"]
schoolspending["Overall_Passing_Rate"] = (schoolspending["Students_Passed_Reading"] + schoolspending["Students_Passed_Math"])/(schoolspending["size"]*2)

schoolspending.rename(columns = {'school_name':'School Name'}, inplace = True)
schoolspending.rename(columns = {'type':'School Type'}, inplace = True)
schoolspending.rename(columns = {'size':'Total Students'}, inplace = True)
schoolspending.rename(columns = {'budget':'Budget (Total)'}, inplace = True)
schoolspending.rename(columns = {'budget_per_student':'Budget (Per Student)'}, inplace = True)
schoolspending.rename(columns = {'math_score':'Average Math Score'}, inplace = True)
schoolspending.rename(columns = {'reading_score':'Average Reading Score'}, inplace = True)
schoolspending.rename(columns = {'Students_Passed_Math':'Students Passed Math (Total)'}, inplace = True)
schoolspending.rename(columns = {'Students_Passed_Reading':'Students Passed Reading (Total)'}, inplace = True)
schoolspending.rename(columns = {'Students_Passed_Math(%)':'Students Passed Math (%)'}, inplace = True)
schoolspending.rename(columns = {'Students_Passed_Reading(%)':'Students Passed Reading (%)'}, inplace = True)
schoolspending.rename(columns = {'Overall_Passing_Rate':'Overall Passing Rate'}, inplace = True)

schoolspending.style.format({
    'Overall Passing Rate': '{:,.2%}'.format,
    'Students Passed Math (%)': '{:,.2%}'.format,
    'Students Passed Reading (%)': '{:,.2%}'.format,
    'Total Students': '{:,.0f}'.format,
    'Budget (Total)': '${:,.0f}'.format,
    'Students Passed Math (Total)': '{:,.0f}'.format,
    'Students Passed Reading (Total)': '{:,.0f}'.format,
    'Total Schools': '{:,.0f}'.format,
})


# In[188]:


#SCORES BY SCHOOL SIZE

#add in scores by school size bands to students table
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

students_df["School Size"] = pd.cut(students_df["size"], size_bins, labels=group_names)

#get count of students for size bins
countstudents_sizebin = students_df.groupby("School Size", as_index=False)["size"].count()

#gets average of math scores for size bins
avgmath_sizebin = students_df.groupby("School Size", as_index=False)["math_score"].mean()

#gets average of reading scores for size bins
avgreading_sizebin = students_df.groupby("School Size", as_index=False)["reading_score"].mean()

#counts number of students who passed math for size bins
countmath_sizebin = students_df[students_df["Pass/Fail_math"] == "Pass"].groupby("School Size", as_index=False).count()
countmath_sizebin = countmath_sizebin.rename(columns = {"Student ID":"Students_Passed_Math"})

#counts number of students who passed reading for size bins
countreading_sizebin = students_df[students_df["Pass/Fail_reading"] == "Pass"].groupby("School Size", as_index=False).count()
countreading_sizebin = countreading_sizebin.rename(columns = {"Student ID":"Students_Passed_Reading"})

#merge average reading and math scores to create summary table
schoolsize = pd.merge(avgmath_sizebin,avgreading_sizebin,how="left", on = ["School Size","School Size"])

#add count of students that passed math to summary table
schoolsize = pd.merge(schoolsize,countmath_sizebin[["School Size","Students_Passed_Math"]],how="left", on = ["School Size","School Size"])

#add count of students that passed reading to summary table
schoolsize = pd.merge(schoolsize,countreading_sizebin[["School Size","Students_Passed_Reading"]],how="left", on = ["School Size","School Size"])

#add school size to summary table
schoolsize = pd.merge(countstudents_sizebin,schoolsize,how="left", on = ["School Size","School Size"])

#% students that passed
schoolsize["Students_Passed_Math(%)"] = schoolsize["Students_Passed_Math"]/schoolsize["size"]
schoolsize["Students_Passed_Reading(%)"] = schoolsize["Students_Passed_Reading"]/schoolsize["size"]
schoolsize["Overall_Passing_Rate"] = (schoolsize["Students_Passed_Reading"] + schoolsize["Students_Passed_Math"])/(schoolsize["size"]*2)

schoolsize.rename(columns = {'school_name':'School Name'}, inplace = True)
schoolsize.rename(columns = {'type':'School Type'}, inplace = True)
schoolsize.rename(columns = {'size':'Total Students'}, inplace = True)
schoolsize.rename(columns = {'budget':'Budget (Total)'}, inplace = True)
schoolsize.rename(columns = {'budget_per_student':'Budget (Per Student)'}, inplace = True)
schoolsize.rename(columns = {'math_score':'Average Math Score'}, inplace = True)
schoolsize.rename(columns = {'reading_score':'Average Reading Score'}, inplace = True)
schoolsize.rename(columns = {'Students_Passed_Math':'Students Passed Math (Total)'}, inplace = True)
schoolsize.rename(columns = {'Students_Passed_Reading':'Students Passed Reading (Total)'}, inplace = True)
schoolsize.rename(columns = {'Students_Passed_Math(%)':'Students Passed Math (%)'}, inplace = True)
schoolsize.rename(columns = {'Students_Passed_Reading(%)':'Students Passed Reading (%)'}, inplace = True)
schoolsize.rename(columns = {'Overall_Passing_Rate':'Overall Passing Rate'}, inplace = True)

schoolsize.style.format({
    'Overall Passing Rate': '{:,.2%}'.format,
    'Students Passed Math (%)': '{:,.2%}'.format,
    'Students Passed Reading (%)': '{:,.2%}'.format,
    'Total Students': '{:,.0f}'.format,
    'Budget (Total)': '${:,.0f}'.format,
    'Students Passed Math (Total)': '{:,.0f}'.format,
    'Students Passed Reading (Total)': '{:,.0f}'.format,
    'Total Schools': '{:,.0f}'.format,
})


# In[ ]:





# In[ ]:





# In[ ]:




