SET IDENTITY_INSERT [auth_group] ON 

INSERT [auth_group] ([id], [name]) VALUES (3, N'employee_change')
INSERT [auth_group] ([id], [name]) VALUES (4, N'employee_reader')
INSERT [auth_group] ([id], [name]) VALUES (6, N'market_change')
INSERT [auth_group] ([id], [name]) VALUES (7, N'market_reader')
INSERT [auth_group] ([id], [name]) VALUES (1, N'org_change')
INSERT [auth_group] ([id], [name]) VALUES (2, N'org_reader')
INSERT [auth_group] ([id], [name]) VALUES (5, N'user_admin')
SET IDENTITY_INSERT [auth_group] OFF
