q_dl_table = """
{% autoescape off %}
select top {{ rows }} {{ fields }}
--from [Cursor_rpt_LK].dbo.v_Tender_Contract s (nolock)
from 
( SELECT DISTINCT
	t.PublDt,
	t.TendDt,
	t.NotifNr,
	t.FZ_FK,
	t.SrcInf,
	t.TendNm,
	t.TenderPrice,
	t.SmallBusiness,
	t.StatusT_Name,
	t.FormT_ID,
	t.FormT_Name,
	t.FONm,
	t.FO_ID,
	t.RegNm,
	t.City_ID,
	t.City_Name,
	t.Cust_ID,
	t.Org_CustINN,
	t.Org_CustNm,
	t.Org_SubCustINN,
	t.Planned,
	t.SubCust_ID,
	t.Org_SubCustNm,
	t.ProviderT_ID,
	t.Org_ProviderINN,
	t.Org_ProviderNm,
	t.ClaimReglament,
	t.ClaimDtBeg,
	t.ClaimDtEnd,
	t.Budgets_Name,
	t.TenderDocReglament,
	t.PaymentReglament,
	t.Tender_Lot,
	t.PrefRus,
	t.BudgetProg_Name,
	t.BudgetProg_FK,
	t.LotNr,
	t.LotStat,
	t.LotNm,
	t.SpecCount,
	t.LFONm,
	t.LotRegNm,
	t.PriceStart,
	ISNULL(c.Cust_Name,t.ConsigneeNm) ConsigneeNm,
	ISNULL(c.Cust_INN,t.ConsigneeInfo) ConsigneeInfo,
	t.PlanTName,
	t.PlanTYear,
	t.PlanTVal,
	t.SupplyDt,
	t.ContrExpVal,
	t.ClaimObesp,
	t.ContrObesp,
	t.MonoMNN,
	t.SupplierGroup_Name,
	t.WinnerOrgINN,
	t.WinnerOrg,
	t.WinnerInfo,
	t.PriceMax,
	t.SecondOrgINN,
	t.SecondOrgNm,
	t.SecordOrgInfo,
	t.PriceOther,
	t.ThirdOrgINN,
	t.ThirdOrgNm,
	t.ThirdOrgInfo,
	t.PriceThird,
	t.FourthOrgINN,
	t.FourthOrgNm,
	t.FourthOrgInfo,
	t.PriceFourth,
	t.LotSpec_Pos,
	t.Innr,
	t.TradeNmR,
	t.ProdNm,
	t.Form,
	t.ShortName,
	t.Price,
	t.Num,
	t.Summa,
	t.ATCID,
	'№ ' + ISNULL(c1.RegNumber,c.RegNumber) as ContractNr,
	ISNULL(c1.SignedDate,c.SignedDate) as ContractDate,
	ISNULL(c1.Url,c.Url) as ContractURL,
	ISNULL(c1.Price,c.Price) as ContractPrice,
	c1.ItemName as ContractItemNm,
	c1.ItemForma as ItemForma,
	c1.ItemUnit as ContractItemUnit,
	c1.ItemPrice as ContractItemPrice,
	c1.ItemCount as ContractItemCount,
	c1.ItemSum as ContractItemSum,
	c1.IntlName,
	c1.TradeName,
	c1.VendorName,
	t.Order_InnNx,
	t.InnNx,
	t.Order_InnR,
	t.TradeNx,
	t.Order_TradeNmNx,
	t.Order_TradeNmR,
	t.Order_Form,
	t.Order_Dosage,
	t.Order_Package,
	t.Order_PrimSize,
	t.Order_BatchSize,
	t.Order_Vendor,
	t.Order_Descr,
	t.Order_Unit,
	t.Order_Price,
	t.Order_Count,
	t.Order_Sum,
	t.Order_AVG_Price,
	t.Ship_FinalPrice,
	t.PriceDropPercentage,
	t.Tender_ID,
	t.Lot_ID,
	t.LotSpec_ID,
	ISNULL(c1.Contract_ID,c.Contract_ID) as Contract_ID,
	c1.Item_ID,
	t.ProdType_ID,
	t.StatusT_ID,
	t.Reg_ID,
	t.DTCreate,
	t.PublDt as [Published]
      ,c1.[Ship_Form]
      ,c1.[Ship_Dosage]
      ,c1.[Ship_Volume]
      ,c1.[Ship_PrimSize]
      ,c1.[Ship_BatchSize]
      ,c1.[Ship_Vendor]
      ,c1.[Ship_Descr]
      ,'Упак.' as Ship_Unit
      ,isnull(c1.[Ship_Price],c1.[ItemPrice]) as Ship_Price
      ,isnull(CAST(c1.[Ship_Count] as bigint),c1.[ItemCount]) as Ship_Count
--      ,isnull(c1.[Ship_Count],c1.[ItemCount]) as Ship_Count
      ,isnull(c1.[Ship_Sum],c1.[ItemSum]) as Ship_Sum 
	  ,c1.ATCID ATCID_Con
	  ,t.Winner_ID
	  ,t.SecondParticipant_ID
	  ,t.ReasonFailure
	  ,ISNULL(c.ConsigneeType,t.ConsigneeType) ConsigneeType
	  ,t.Budgets_ID
	  ,DTSynchronization
	  ,LotReg_ID
--	  ,ISNULL(ISNULL(c.Dod_ID, c1.Dod_ID), t.Dod_ID) as Dod_ID
	  ,t.Dod_ID as Dod_ID
      ,d.[DrugFormID_Group_AVG]
      ,d.[DosageNmR_norm]
      ,d.[Pack1ID_Group]
      ,d.[PackMV]
      ,d.[QPack]
      ,d.[VendorID]
      ,d.[VendorCountryID]
FROM [Cursor_rpt_LK].dbo.ComplexRpt_CACHE t (nolock)
LEFT JOIN [Cursor_rpt_LK].dbo.ComplexRpt_CACHE_Dod d (nolock) ON t.dod_ID = d.id_dod
LEFT JOIN [Cursor_rpt_LK].dbo.ComplexRpt_CACHE_Contract c (nolock) 
	ON c.Lot_ID = t.Lot_ID 
	   and c.Contract_ID > 0
	   and c.Lotspec_ID IS NULL
LEFT JOIN [Cursor_rpt_LK].dbo.ComplexRpt_CACHE_Contract c1 (nolock) 
	ON c1.LotSpec_ID = t.LotSpec_ID 
	   and c1.Contract_ID > 0
	   and isnull(c1.LotSpec_ID,0) > 0
WHERE (t.Reg_ID < 100) AND (t.ProdType_ID = 'L')
) s 
{% if filters %}where {{ filters }} {% endif %}
{% endautoescape %}
"""