USE [CursorTest]
GO
SET IDENTITY_INSERT [dbo].[db_org] ON 

INSERT [dbo].[db_org] ([id], [name], [sync_time], [sync_flag]) VALUES (1, N'Takeda', N'01:00', 0)
INSERT [dbo].[db_org] ([id], [name], [sync_time], [sync_flag]) VALUES (2, N'ОптоФарм', NULL, 0)
INSERT [dbo].[db_org] ([id], [name], [sync_time], [sync_flag]) VALUES (4, N'Тестовая', NULL, 0)
INSERT [dbo].[db_org] ([id], [name], [sync_time], [sync_flag]) VALUES (6, N'Шайер рус', N'02:00', 0)
SET IDENTITY_INSERT [dbo].[db_org] OFF
