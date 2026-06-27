# DB-Models
> Decision statements
    user would lead the main core table with all users listing with protection with admin unit
    Making easy and unified feild to query for information
    Linking assets for refrences and information sharing

User : [ admin, student, company ]
    |- Profile information
    |- account-status [active/freezed]
    |- assets-link [ linking assets of user ]

doc-elements || Simple refrence unit for documents from company and student for their document needs
    |- user_id
    |- blob_unit


event-drive : [job, internship, hiring hacathon]
    |- Event Information document
    |- Meta-data
    |- Deadline

application
    |- applied to : company id
    |- applied by : student id
    |- resume-document
    |- status [shortlisted, selected, rejected]
    |- created time stamp [racing conditions and deadline conflicts]

