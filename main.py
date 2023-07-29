from bs4 import BeautifulSoup
import requests

# with open("citilinkdata.json") as fp:
s = requests.post('https://www.citilink.ru/graphql/', json={
    "query": "query GetProductHeader($filter:Catalog_ProductFilterInput!,$actionsInput:Action_ProductActionsInput!,$courierDeliveryInput:Catalog_ProductCourierDeliveryVariantsInput!){product(filter:$filter){id,slug,name,isAvailable,shortName,description,rating,multiplicity,searchDescription,images{citilink{...Image},discount{...Image}},images3d{...Image},price{...ProductPriceFull},videos{...Video},stock{lastAvailableTime},marks{fairMark},hidingSettings{isFeedbacksHidden,isReviewsHidden},social{discussionsCount,feedbacksCount,reviewsCount,videosCount},category{...CategoryWithParents},brand{...ProductBrand},credit{...ProductCreditProgram},labels{...ProductLabel},propertiesShort{id,name,description,value,measure},configuration{isInConfiguration,canBeAddedToCurrentConfiguration},actions(input:$actionsInput){items{...ProductActionItem}},delivery{self{...ProductSelfDelivery},courier{variants(input:$courierDeliveryInput){...ProductCourierDeliveryItem}}}}}fragment Image on Image{sources{url,size}}fragment ProductPriceFull on Catalog_ProductPrice{...ProductPrice,isFairPrice,bonusPoints}fragment ProductPrice on Catalog_ProductPrice{current,old,club,clubPriceViewType}fragment Video on Catalog_Video{id,title,youtube{id,preview{...Image}}}fragment CategoryWithParents on Catalog_Category{...Category,parents{...Category}}fragment Category on Catalog_Category{id,name,slug}fragment ProductBrand on Catalog_Brand{id,name,slug}fragment ProductCreditProgram on Catalog_CreditProgram{credit{...ProductCredit},installment{...ProductCredit}}fragment ProductCredit on Catalog_Credit{name,period,payment}fragment ProductLabel on Catalog_Label{id,type,title,description,target{...Target},textColor,backgroundColor,expirationTime}fragment Target on Catalog_Target{action{...TargetAction},url,inNewWindow}fragment TargetAction on Catalog_TargetAction{id}fragment ProductActionItem on Action_Action{id,type{name,type},shortDescription,disclaimer}fragment ProductSelfDelivery on Catalog_ProductSelfDelivery{availabilityByDays{deliveryTime,storeCount}}fragment ProductCourierDeliveryItem on Catalog_ProductCourierDeliveryVariant{deliveryTime,id,type,price}",
    "variables": {
        "filter": {
            "id": "1048584"
        },
        "actionsInput": {
            "limit": 10
        },
        "courierDeliveryInput": {
            "filter": {
                "types": [
                    "FAST",
                    "TODAY",
                    "STANDARD"
                ]
            }
        }
    }
})
x = s.json()
print(x)
