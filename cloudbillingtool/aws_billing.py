import pandas as pd
import csv
from pyspark import rdd, Row
from pyspark.pandas import DataFrame
from pyspark.sql.types import StructType, StringType
from pyspark.sql.functions import col, lit, to_date, explode
from . import helper

# EXAMPLE
# INPUT
#identity/LineItemId,identity/TimeInterval,bill/InvoiceId,bill/InvoicingEntity,bill/BillingEntity,bill/BillType,bill/PayerAccountId,bill/BillingPeriodStartDate,bill/BillingPeriodEndDate,lineItem/UsageAccountId,lineItem/LineItemType,lineItem/UsageStartDate,lineItem/UsageEndDate,lineItem/ProductCode,lineItem/UsageType,lineItem/Operation,lineItem/AvailabilityZone,lineItem/ResourceId,lineItem/UsageAmount,lineItem/NormalizationFactor,lineItem/NormalizedUsageAmount,lineItem/CurrencyCode,lineItem/UnblendedRate,lineItem/UnblendedCost,lineItem/BlendedRate,lineItem/BlendedCost,lineItem/LineItemDescription,lineItem/TaxType,lineItem/LegalEntity,product/ProductName,product/abdInstanceClass,product/alarmType,product/availabilityZone,product/capacitystatus,product/classicnetworkingsupport,product/clockSpeed,product/currentGeneration,product/dedicatedEbsThroughput,product/description,product/ecu,product/endpointType,product/enhancedNetworkingSupported,product/eventType,product/fromLocation,product/fromLocationType,product/fromRegionCode,product/gpuMemory,product/group,product/groupDescription,product/indexingSource,product/instance,product/instanceFamily,product/instanceType,product/instanceTypeFamily,product/intelAvx2Available,product/intelAvxAvailable,product/intelTurboAvailable,product/licenseModel,product/location,product/locationType,product/logsDestination,product/marketoption,product/maxIopsBurstPerformance,product/maxIopsvolume,product/maxThroughputvolume,product/maxVolumeSize,product/memory,product/networkPerformance,product/normalizationSizeFactor,product/operatingSystem,product/operation,product/physicalProcessor,product/platousagetype,product/preInstalledSw,product/processorArchitecture,product/processorFeatures,product/productFamily,product/protocol,product/region,product/regionCode,product/servicecode,product/servicename,product/sku,product/storage,product/storageMedia,product/tenancy,product/tenancySupport,product/toLocation,product/toLocationType,product/toRegionCode,product/transferType,product/usagetype,product/vcpu,product/version,product/volumeApiName,product/volumeType,product/vpcnetworkingsupport,pricing/RateCode,pricing/RateId,pricing/currency,pricing/publicOnDemandCost,pricing/publicOnDemandRate,pricing/term,pricing/unit,reservation/AmortizedUpfrontCostForUsage,reservation/AmortizedUpfrontFeeForBillingPeriod,reservation/EffectiveCost,reservation/EndTime,reservation/ModificationStatus,reservation/NormalizedUnitsPerReservation,reservation/NumberOfReservations,reservation/RecurringFeeForUsage,reservation/StartTime,reservation/SubscriptionId,reservation/TotalReservedNormalizedUnits,reservation/TotalReservedUnits,reservation/UnitsPerReservation,reservation/UnusedAmortizedUpfrontFeeForBillingPeriod,reservation/UnusedNormalizedUnitQuantity,reservation/UnusedQuantity,reservation/UnusedRecurringFee,reservation/UpfrontValue,savingsPlan/TotalCommitmentToDate,savingsPlan/SavingsPlanARN,savingsPlan/SavingsPlanRate,savingsPlan/UsedCommitment,savingsPlan/SavingsPlanEffectiveCost,savingsPlan/AmortizedUpfrontCommitmentForBillingPeriod,savingsPlan/RecurringCommitmentForBillingPeriod
#nfrteyjoycnvt5vttmxjqxe5m6lothxuv4vduqtzs6fbkgxsiaga,2023-03-01T00:00:00Z/2023-03-31T23:59:59Z,,Amazon Web Services EMEA SARL,AWS,Anniversary,455634372357,2023-03-01T00:00:00Z,2023-04-01T00:00:00Z,455634372357,Fee,2023-03-01T00:00:00Z,2023-03-31T23:59:59Z,AWSDeveloperSupport,,,,,0.0000000000,,,USD,,29.0000000000,,29.0000000000,Recurring Fee,,Amazon Web Services EMEA SARL,AWS Support (Developer),,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,0.0000000000,,,,,,,,,,,,,1965504544,,,,,,,,,,,,,,,
#l35hakn3f7f3akvdxdiybetp7kepqn2ixi44c6tzntqs5r4j6pea,2023-03-01T00:00:00Z/2023-04-01T00:00:00Z,,Amazon Web Services EMEA SARL,AWS,Anniversary,455634372357,2023-03-01T00:00:00Z,2023-04-01T00:00:00Z,455634372357,Tax,2023-03-01T00:00:00Z,2023-04-01T00:00:00Z,AWSDataTransfer,,,,,1.0000000000,,,USD,,0.0000000000,,0.0000000000,Tax for product code AWSDataTransfer,VAT,Amazon Web Services EMEA SARL,AWS Data Transfer,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,0.0000000000,,,,,,,,,,,,,,,,,,,,,,,,,,,,
#ypkij3oyar7hjkozdjj3v43kbb6md7osrcmk76t2g7tjyg24wd5a,2023-03-01T00:00:00Z/2023-04-01T00:00:00Z,,Amazon Web Services EMEA SARL,AWS,Anniversary,455634372357,2023-03-01T00:00:00Z,2023-04-01T00:00:00Z,455634372357,Tax,2023-03-01T00:00:00Z,2023-04-01T00:00:00Z,AWSGlue,,,,,1.0000000000,,,USD,,0.0000000000,,0.0000000000,Tax for product code AWSGlue,VAT,Amazon Web Services EMEA SARL,AWS Glue,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,0.0000000000,,,,,,,,,,,,,,,,,,,,,,,,,,,,


aws_schema = StructType() \
  .add("identity_LineItemId", StringType(), True) \
  .add("identity_TimeInterval", StringType(), True) \
  .add("bill_InvoiceId", StringType(), True) \
  .add("bill_InvoicingEntity", StringType(), True) \
  .add("bill_BillingEntity", StringType(), True) \
  .add("bill_BillType", StringType(), True) \
  .add("bill_PayerAccountId", StringType(), True) \
  .add("bill_BillingPeriodStartDate", StringType(), True) \
  .add("bill_BillingPeriodEndDate", StringType(), True) \
  .add("lineItem_UsageAccountId", StringType(), True) \
  .add("lineItem_LineItemType", StringType(), True) \
  .add("lineItem_UsageStartDate", StringType(), True) \
  .add("lineItem_UsageEndDate", StringType(), True) \
  .add("lineItem_ProductCode", StringType(), True) \
  .add("lineItem_UsageType", StringType(), True) \
  .add("lineItem_Operation", StringType(), True) \
  .add("lineItem_AvailabilityZone", StringType(), True) \
  .add("lineItem_ResourceId", StringType(), True) \
  .add("lineItem_UsageAmount", StringType(), True) \
  .add("lineItem_NormalizationFactor", StringType(), True) \
  .add("lineItem_NormalizedUsageAmount", StringType(), True) \
  .add("lineItem_CurrencyCode", StringType(), True) \
  .add("lineItem_UnblendedRate", StringType(), True) \
  .add("lineItem_UnblendedCost", StringType(), True) \
  .add("lineItem_BlendedRate", StringType(), True) \
  .add("lineItem_BlendedCost", StringType(), True) \
  .add("lineItem_LineItemDescription", StringType(), True) \
  .add("lineItem_TaxType", StringType(), True) \
  .add("lineItem_LegalEntity", StringType(), True) \
  .add("product_ProductName", StringType(), True) \
  .add("product_abdInstanceClass", StringType(), True) \
  .add("product_alarmType", StringType(), True) \
  .add("product_availabilityZone", StringType(), True) \
  .add("product_capacitystatus", StringType(), True) \
  .add("product_classicnetworkingsupport", StringType(), True) \
  .add("product_clockSpeed", StringType(), True) \
  .add("product_currentGeneration", StringType(), True) \
  .add("product_dedicatedEbsThroughput", StringType(), True) \
  .add("product_description", StringType(), True) \
  .add("product_ecu", StringType(), True) \
  .add("product_endpointType", StringType(), True) \
  .add("product_enhancedNetworkingSupported", StringType(), True) \
  .add("product_eventType", StringType(), True) \
  .add("product_fromLocation", StringType(), True) \
  .add("product_fromLocationType", StringType(), True) \
  .add("product_fromRegionCode", StringType(), True) \
  .add("product_gpuMemory", StringType(), True) \
  .add("product_group", StringType(), True) \
  .add("product_groupDescription", StringType(), True) \
  .add("product_indexingSource", StringType(), True) \
  .add("product_instance", StringType(), True) \
  .add("product_instanceFamily", StringType(), True) \
  .add("product_instanceType", StringType(), True) \
  .add("product_instanceTypeFamily", StringType(), True) \
  .add("product_intelAvx2Available", StringType(), True) \
  .add("product_intelAvxAvailable", StringType(), True) \
  .add("product_intelTurboAvailable", StringType(), True) \
  .add("product_licenseModel", StringType(), True) \
  .add("product_location", StringType(), True) \
  .add("product_locationType", StringType(), True) \
  .add("product_logsDestination", StringType(), True) \
  .add("product_marketoption", StringType(), True) \
  .add("product_maxIopsBurstPerformance", StringType(), True) \
  .add("product_maxIopsvolume", StringType(), True) \
  .add("product_maxThroughputvolume", StringType(), True) \
  .add("product_maxVolumeSize", StringType(), True) \
  .add("product_memory", StringType(), True) \
  .add("product_networkPerformance", StringType(), True) \
  .add("product_normalizationSizeFactor", StringType(), True) \
  .add("product_operatingSystem", StringType(), True) \
  .add("product_operation", StringType(), True) \
  .add("product_physicalProcessor", StringType(), True) \
  .add("product_platousagetype", StringType(), True) \
  .add("product_preInstalledSw", StringType(), True) \
  .add("product_processorArchitecture", StringType(), True) \
  .add("product_processorFeatures", StringType(), True) \
  .add("product_productFamily", StringType(), True) \
  .add("product_protocol", StringType(), True) \
  .add("product_region", StringType(), True) \
  .add("product_regionCode", StringType(), True) \
  .add("product_servicecode", StringType(), True) \
  .add("product_servicename", StringType(), True) \
  .add("product_sku", StringType(), True) \
  .add("product_storage", StringType(), True) \
  .add("product_storageMedia", StringType(), True) \
  .add("product_tenancy", StringType(), True) \
  .add("product_tenancySupport", StringType(), True) \
  .add("savingsPlan_SavingsPlanARN", StringType(), True) \
  .add("savingsPlan_SavingsPlanRate", StringType(), True) \
  .add("savingsPlan_UsedCommitment", StringType(), True) \
  .add("savingsPlan_SavingsPlanEffectiveCost", StringType(), True) \
  .add("savingsPlan_AmortizedUpfrontCommitmentForBillingPeriod", StringType(), True) \
  .add("savingsPlan_RecurringCommitmentForBillingPeriod", StringType(), True)


def load_files(spark, aws_data, work_folder ) -> rdd :
    #resource_mapping_df = pd.read_csv(work_folder+"/resource_mapping.csv", sep='\t')
    #type_mapping_df = pd.read_csv(work_folder+"/type_mapping.csv", sep='\t')
    
    return\
        spark.read\
        .options(format='csv', escape="\"", header=True)\
        .schema(aws_schema)\
        .csv(aws_data)\
        .rdd \
        .map(lambda row: {
            "Provider": "aws",
            "Type":  "",
            "Costs": row.lineItem_UnblendedCost,
            "UnitPrice": row.lineItem_UnblendedRate,
            "Quantity": row.lineItem_UsageAmount,
            "Product": row.product_ProductName,
            "Date": row.bill_BillingPeriodStartDate,
            "CostResourceID": row.lineItem_ResourceId,
            "CostResourceTag": [""], # Todo select Tag from AWS export file
            "ProductTag": [""]
            # "CostResourceTag": list(set(
            #     [""] +
            #     # no TypeMapping for Azure
            #     # only mapping for CostRsourceId
            #     list(resource_mapping_df.loc[resource_mapping_df['CostResourceID'] \
            #          .str.contains(row.ResourceId)]['CostResourceTag'])
            #     # filter resourceMapping for costresourceid
            # )),
            # "ProductTag": list(set([""]+resource_mapping_df.loc[resource_mapping_df['CostResourceID'].str.contains(
            #     helper.extract_costresourceid(row.ProductName))]['ProductTag']))
      })


def load_files_with_mapping(spark, aws_data, metadata_folder):

    aws_df: DataFrame = \
        load_files(spark, aws_data, metadata_folder+"/mappingfiles")\
        .toDF()\
        .alias("aws_df") \
    
    aws_df_with_types = aws_df \
        .select(lit("aws").alias("Provider"),
                col("aws_df.Type"),
                col("aws_df.Product").alias("ProductName"),
                col("aws_df.Costs").cast("float").alias("Costs"),
                col("aws_df.UnitPrice").cast("float").alias("UnitPrice"),
                col("aws_df.Quantity").cast("float").alias("Quantity"),
                to_date(col("aws_df.Date"), "yyyy-MM-dd'T'HH:mm:ss'Z'").alias("Date"),
                col("aws_df.CostResourceID").alias("CostResourceID"),
                col("aws_df.CostResourceTag").alias("CostResourceTag"),
                col("aws_df.ProductTag").alias("ProductTag"))

    return aws_df_with_types
