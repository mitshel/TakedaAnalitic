USE [BIMonitor]
GO
/****** Object:  UserDefinedFunction [dbo].[fnParseList]    Script Date: 06.11.2018 22:27:07 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER FUNCTION [dbo].[fnParseList](@List varchar(max))
RETURNS @Output TABLE
( Sequence int IDENTITY(1,1),
Item varchar(4096) )
AS
BEGIN
DECLARE @Pointer int
SET @Pointer = 0
WHILE (LEN(@List) > 0)
BEGIN
SET @Pointer = CHARINDEX(',', @List)
IF (@Pointer = 0) AND (LEN(@List) > 0)
  BEGIN
    INSERT @Output VALUES (@List)
    BREAK
  END
IF (@Pointer > 1)
  BEGIN
    INSERT @Output VALUES (LEFT(@List, @Pointer - 1))
    SET @List = RIGHT(@List, (LEN(@List) - @Pointer))
  END
ELSE
  SET @List = RIGHT(@List, (LEN(@List) - @Pointer))
END
RETURN
END
