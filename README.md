# Plagiarism Detection System
This is a Django Web application for detecting plagiarism in student homework.
# Description
By default, this system groups users into two categories: teachers and students. Since teachers are in charge of the supervision of students' homework, we grant teachers a higher level of authorization and thus more functionalities.

As for the storage structure of homework files, we organize homework text files under different assignment topics. For example, a teacher can create a "Chapter 3 - Newton's Method" folder and all homework files uploaded regarding this topic are stored into that folder.

# Functionalities for Teachers
Teachers are able to manage all student accounts, including activating accounts or moving accounts into the blacklist.
Teachers can search, modify or delete any text files under his assignment topics.
Teachers can perform a plagiarism detection check based on text similarity calculation.
If the text similarity between two text files are greater than a threshold, a spot of plagiarism is found. Teachers can go on and take a look inside the similar sentences which are marked out in these files.
# Functionalities for Students
Students can upload their homework text files under an assignment topic.
Students can modify or delete their homework files.

# System flow
Given the above methods, we can construct our plagiarism detection work flow as below:

Generate SimHash digital fingerprints for all homework text blocks. Perform cross comparison on these fingerprints to quickly pick out the suspicious pairs.
Calculate various text similarity coefficients after stop-word removal. If these coefficients exceed a certain threshold, the system will judge them as a plagiarized pair.
The system will look into this pair and scan through all sentences to pick out the plagiarized sentences with string matching methods.

# Tools
Python 3
Python is an interpreted, high-level, general-purpose programming language. As a dynamically typed language, Python is more flexible and it encourages problem solving with different methods. Additionally, Python is more error-tolerant when minor mistakes occur.

# Django
Django is a Python-based free and open-source web framework, which follows the model-template-view (MTV) architectural pattern. It encourages rapid development and pragmatic design with a support to avoid common security problems.
# Bootstrap
Bootstrap is a free and open-source CSS framework directed at responsive, mobile-first front-end web development. It also provides an easy and userful set of rules on grids and layouts operations.

# SQLite 3
SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine. The SQLite file format is stable, cross-platform, and backwards compatible.

<img src="C:\Users\X280\Downloads\hacker rank plagarism\Plagiarism-Detection\PlagDetec\images\rajesh.jpg">
