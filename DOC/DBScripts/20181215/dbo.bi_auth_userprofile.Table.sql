USE [CursorTest]
GO
SET IDENTITY_INSERT [dbo].[bi_auth_userprofile] ON 

INSERT [dbo].[bi_auth_userprofile] ([id], [is_orgadmin], [user_id]) VALUES (1, 0, 3)
INSERT [dbo].[bi_auth_userprofile] ([id], [is_orgadmin], [user_id]) VALUES (2, 1, 4)
INSERT [dbo].[bi_auth_userprofile] ([id], [is_orgadmin], [user_id]) VALUES (3, 0, 6)
INSERT [dbo].[bi_auth_userprofile] ([id], [is_orgadmin], [user_id]) VALUES (4, 1, 7)
SET IDENTITY_INSERT [dbo].[bi_auth_userprofile] OFF
