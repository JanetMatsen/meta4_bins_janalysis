DROP TABLE IF EXISTS summary_meta4_part1;
CREATE TABLE summary_meta4_part1 AS SELECT m.genome, g.locus_tag, g.product, ROUND(LakWasM100_LOW12_2.reads_mapped) AS LakWasM100_LOW12_2, ROUND(LakWasM103_HOW12_2.reads_mapped) AS LakWasM103_HOW12_2, ROUND(LakWasM104_HOW12_2.reads_mapped) AS LakWasM104_HOW12_2, ROUND(LakWasM105_HOW12_2.reads_mapped) AS LakWasM105_HOW12_2, ROUND(LakWasM106_HOW12_2.reads_mapped) AS LakWasM106_HOW12_2, ROUND(LakWasM109_LOW13_2.reads_mapped) AS LakWasM109_LOW13_2, ROUND(LakWasM110_LOW13_2.reads_mapped) AS LakWasM110_LOW13_2, ROUND(LakWasM111_LOW13_2.reads_mapped) AS LakWasM111_LOW13_2, ROUND(LakWasM112_LOW13_2.reads_mapped) AS LakWasM112_LOW13_2, ROUND(LakWasM115_HOW13_2.reads_mapped) AS LakWasM115_HOW13_2, ROUND(LakWasM116_HOW13_2.reads_mapped) AS LakWasM116_HOW13_2, ROUND(LakWasM117_HOW13_2.reads_mapped) AS LakWasM117_HOW13_2, ROUND(LakWasM118_HOW13_2.reads_mapped) AS LakWasM118_HOW13_2, ROUND(LakWasM121_LOW14_2.reads_mapped) AS LakWasM121_LOW14_2, ROUND(LakWasM122_LOW14_2.reads_mapped) AS LakWasM122_LOW14_2, ROUND(LakWasM123_LOW14_2.reads_mapped) AS LakWasM123_LOW14_2, ROUND(LakWasM124_LOW14_2.reads_mapped) AS LakWasM124_LOW14_2, ROUND(LakWasM127_HOW14_2.reads_mapped) AS LakWasM127_HOW14_2, ROUND(LakWasM128_HOW14_2.reads_mapped) AS LakWasM128_HOW14_2, ROUND(LakWasM129_HOW14_2.reads_mapped) AS LakWasM129_HOW14_2, ROUND(LakWasM130_HOW14_2.reads_mapped) AS LakWasM130_HOW14_2, ROUND(LakWasMe73_LOW10_2.reads_mapped) AS LakWasMe73_LOW10_2, ROUND(LakWasMe74_LOW10_2.reads_mapped) AS LakWasMe74_LOW10_2, ROUND(LakWasMe75_LOW10_2.reads_mapped) AS LakWasMe75_LOW10_2, ROUND(LakWasMe76_LOW10_2.reads_mapped) AS LakWasMe76_LOW10_2, ROUND(LakWasMe79_HOW10_2.reads_mapped) AS LakWasMe79_HOW10_2, ROUND(LakWasMe80_HOW10_2.reads_mapped) AS LakWasMe80_HOW10_2, ROUND(LakWasMe81_HOW10_2.reads_mapped) AS LakWasMe81_HOW10_2, ROUND(LakWasMe82_HOW10_2.reads_mapped) AS LakWasMe82_HOW10_2
	FROM genes_isolate_genomes AS g
		LEFT JOIN map_locus_to_organism AS m ON m.locus = g.locus
		LEFT JOIN summary_LakWasM100_LOW12_2 AS LakWasM100_LOW12_2 ON LakWasM100_LOW12_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM103_HOW12_2 AS LakWasM103_HOW12_2 ON LakWasM103_HOW12_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM104_HOW12_2 AS LakWasM104_HOW12_2 ON LakWasM104_HOW12_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM105_HOW12_2 AS LakWasM105_HOW12_2 ON LakWasM105_HOW12_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM106_HOW12_2 AS LakWasM106_HOW12_2 ON LakWasM106_HOW12_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM109_LOW13_2 AS LakWasM109_LOW13_2 ON LakWasM109_LOW13_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM110_LOW13_2 AS LakWasM110_LOW13_2 ON LakWasM110_LOW13_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM111_LOW13_2 AS LakWasM111_LOW13_2 ON LakWasM111_LOW13_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM112_LOW13_2 AS LakWasM112_LOW13_2 ON LakWasM112_LOW13_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM115_HOW13_2 AS LakWasM115_HOW13_2 ON LakWasM115_HOW13_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM116_HOW13_2 AS LakWasM116_HOW13_2 ON LakWasM116_HOW13_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM117_HOW13_2 AS LakWasM117_HOW13_2 ON LakWasM117_HOW13_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM118_HOW13_2 AS LakWasM118_HOW13_2 ON LakWasM118_HOW13_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM121_LOW14_2 AS LakWasM121_LOW14_2 ON LakWasM121_LOW14_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM122_LOW14_2 AS LakWasM122_LOW14_2 ON LakWasM122_LOW14_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM123_LOW14_2 AS LakWasM123_LOW14_2 ON LakWasM123_LOW14_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM124_LOW14_2 AS LakWasM124_LOW14_2 ON LakWasM124_LOW14_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM127_HOW14_2 AS LakWasM127_HOW14_2 ON LakWasM127_HOW14_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM128_HOW14_2 AS LakWasM128_HOW14_2 ON LakWasM128_HOW14_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM129_HOW14_2 AS LakWasM129_HOW14_2 ON LakWasM129_HOW14_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasM130_HOW14_2 AS LakWasM130_HOW14_2 ON LakWasM130_HOW14_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe73_LOW10_2 AS LakWasMe73_LOW10_2 ON LakWasMe73_LOW10_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe74_LOW10_2 AS LakWasMe74_LOW10_2 ON LakWasMe74_LOW10_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe75_LOW10_2 AS LakWasMe75_LOW10_2 ON LakWasMe75_LOW10_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe76_LOW10_2 AS LakWasMe76_LOW10_2 ON LakWasMe76_LOW10_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe79_HOW10_2 AS LakWasMe79_HOW10_2 ON LakWasMe79_HOW10_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe80_HOW10_2 AS LakWasMe80_HOW10_2 ON LakWasMe80_HOW10_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe81_HOW10_2 AS LakWasMe81_HOW10_2 ON LakWasMe81_HOW10_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe82_HOW10_2 AS LakWasMe82_HOW10_2 ON LakWasMe82_HOW10_2.locus_tag = g.locus_tag
WHERE type = 'CDS'
;

DROP TABLE IF EXISTS summary_meta4_part2;
CREATE TABLE summary_meta4_part2 AS SELECT g.locus_tag, ROUND(LakWasMe85_LOW11_2.reads_mapped) AS LakWasMe85_LOW11_2, ROUND(LakWasMe86_LOW11_2.reads_mapped) AS LakWasMe86_LOW11_2, ROUND(LakWasMe87_LOW11_2.reads_mapped) AS LakWasMe87_LOW11_2, ROUND(LakWasMe88_LOW11_2.reads_mapped) AS LakWasMe88_LOW11_2, ROUND(LakWasMe91_HOW11_2.reads_mapped) AS LakWasMe91_HOW11_2, ROUND(LakWasMe92_HOW11_2.reads_mapped) AS LakWasMe92_HOW11_2, ROUND(LakWasMe93_HOW11_2.reads_mapped) AS LakWasMe93_HOW11_2, ROUND(LakWasMe94_HOW11_2.reads_mapped) AS LakWasMe94_HOW11_2, ROUND(LakWasMe97_LOW12_2.reads_mapped) AS LakWasMe97_LOW12_2, ROUND(LakWasMe98_LOW12_2.reads_mapped) AS LakWasMe98_LOW12_2, ROUND(LakWasMe99_LOW12_2.reads_mapped) AS LakWasMe99_LOW12_2, ROUND(LakWasMet10_HOW4_2.reads_mapped) AS LakWasMet10_HOW4_2, ROUND(LakWasMet13_LOW5_2.reads_mapped) AS LakWasMet13_LOW5_2, ROUND(LakWasMet14_LOW5_2.reads_mapped) AS LakWasMet14_LOW5_2, ROUND(LakWasMet15_LOW5_2.reads_mapped) AS LakWasMet15_LOW5_2, ROUND(LakWasMet16_LOW5_2.reads_mapped) AS LakWasMet16_LOW5_2, ROUND(LakWasMet19_HOW5_2.reads_mapped) AS LakWasMet19_HOW5_2, ROUND(LakWasMet20_HOW5_2.reads_mapped) AS LakWasMet20_HOW5_2, ROUND(LakWasMet21_HOW5_2.reads_mapped) AS LakWasMet21_HOW5_2, ROUND(LakWasMet22_HOW5_2.reads_mapped) AS LakWasMet22_HOW5_2, ROUND(LakWasMet25_LOW6_2.reads_mapped) AS LakWasMet25_LOW6_2, ROUND(LakWasMet26_LOW6_2.reads_mapped) AS LakWasMet26_LOW6_2, ROUND(LakWasMet27_LOW6_2.reads_mapped) AS LakWasMet27_LOW6_2, ROUND(LakWasMet28_LOW6_2.reads_mapped) AS LakWasMet28_LOW6_2, ROUND(LakWasMet31_HOW6_2.reads_mapped) AS LakWasMet31_HOW6_2, ROUND(LakWasMet32_HOW6_2.reads_mapped) AS LakWasMet32_HOW6_2, ROUND(LakWasMet33_HOW6_2.reads_mapped) AS LakWasMet33_HOW6_2, ROUND(LakWasMet34_HOW6_2.reads_mapped) AS LakWasMet34_HOW6_2, ROUND(LakWasMet37_LOW7_2.reads_mapped) AS LakWasMet37_LOW7_2, ROUND(LakWasMet38_LOW7_2.reads_mapped) AS LakWasMet38_LOW7_2, ROUND(LakWasMet39_LOW7_2.reads_mapped) AS LakWasMet39_LOW7_2, ROUND(LakWasMet40_LOW7_2.reads_mapped) AS LakWasMet40_LOW7_2, ROUND(LakWasMet43_HOW7_2.reads_mapped) AS LakWasMet43_HOW7_2, ROUND(LakWasMet44_HOW7_2.reads_mapped) AS LakWasMet44_HOW7_2, ROUND(LakWasMet45_HOW7_2.reads_mapped) AS LakWasMet45_HOW7_2, ROUND(LakWasMet46_HOW7_2.reads_mapped) AS LakWasMet46_HOW7_2, ROUND(LakWasMet49_LOW8_2.reads_mapped) AS LakWasMet49_LOW8_2, ROUND(LakWasMet50_LOW8_2.reads_mapped) AS LakWasMet50_LOW8_2, ROUND(LakWasMet51_LOW8_2.reads_mapped) AS LakWasMet51_LOW8_2, ROUND(LakWasMet52_LOW8_2.reads_mapped) AS LakWasMet52_LOW8_2, ROUND(LakWasMet55_HOW8_2.reads_mapped) AS LakWasMet55_HOW8_2, ROUND(LakWasMet56_HOW8_2.reads_mapped) AS LakWasMet56_HOW8_2, ROUND(LakWasMet57_HOW8_2.reads_mapped) AS LakWasMet57_HOW8_2, ROUND(LakWasMet58_HOW8_2.reads_mapped) AS LakWasMet58_HOW8_2, ROUND(LakWasMet61_LOW9_2.reads_mapped) AS LakWasMet61_LOW9_2, ROUND(LakWasMet62_LOW9_2.reads_mapped) AS LakWasMet62_LOW9_2, ROUND(LakWasMet63_LOW9_2.reads_mapped) AS LakWasMet63_LOW9_2, ROUND(LakWasMet64_LOW9_2.reads_mapped) AS LakWasMet64_LOW9_2, ROUND(LakWasMet67_HOW9_2.reads_mapped) AS LakWasMet67_HOW9_2, ROUND(LakWasMet68_HOW9_2.reads_mapped) AS LakWasMet68_HOW9_2, ROUND(LakWasMet69_HOW9_2.reads_mapped) AS LakWasMet69_HOW9_2, ROUND(LakWasMet70_HOW9_2.reads_mapped) AS LakWasMet70_HOW9_2, ROUND(LakWasMeta1_LOW4_2.reads_mapped) AS LakWasMeta1_LOW4_2, ROUND(LakWasMeta2_LOW4_2.reads_mapped) AS LakWasMeta2_LOW4_2, ROUND(LakWasMeta3_LOW4_2.reads_mapped) AS LakWasMeta3_LOW4_2, ROUND(LakWasMeta4_LOW4_2.reads_mapped) AS LakWasMeta4_LOW4_2, ROUND(LakWasMeta7_HOW4_2.reads_mapped) AS LakWasMeta7_HOW4_2, ROUND(LakWasMeta8_HOW4_2.reads_mapped) AS LakWasMeta8_HOW4_2, ROUND(LakWasMeta9_HOW4_2.reads_mapped) AS LakWasMeta9_HOW4_2
	FROM genes_isolate_genomes AS g
		LEFT JOIN map_locus_to_organism AS m ON m.locus = g.locus
		LEFT JOIN summary_LakWasMe85_LOW11_2 AS LakWasMe85_LOW11_2 ON LakWasMe85_LOW11_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe86_LOW11_2 AS LakWasMe86_LOW11_2 ON LakWasMe86_LOW11_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe87_LOW11_2 AS LakWasMe87_LOW11_2 ON LakWasMe87_LOW11_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe88_LOW11_2 AS LakWasMe88_LOW11_2 ON LakWasMe88_LOW11_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe91_HOW11_2 AS LakWasMe91_HOW11_2 ON LakWasMe91_HOW11_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe92_HOW11_2 AS LakWasMe92_HOW11_2 ON LakWasMe92_HOW11_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe93_HOW11_2 AS LakWasMe93_HOW11_2 ON LakWasMe93_HOW11_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe94_HOW11_2 AS LakWasMe94_HOW11_2 ON LakWasMe94_HOW11_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe97_LOW12_2 AS LakWasMe97_LOW12_2 ON LakWasMe97_LOW12_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe98_LOW12_2 AS LakWasMe98_LOW12_2 ON LakWasMe98_LOW12_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMe99_LOW12_2 AS LakWasMe99_LOW12_2 ON LakWasMe99_LOW12_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet10_HOW4_2 AS LakWasMet10_HOW4_2 ON LakWasMet10_HOW4_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet13_LOW5_2 AS LakWasMet13_LOW5_2 ON LakWasMet13_LOW5_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet14_LOW5_2 AS LakWasMet14_LOW5_2 ON LakWasMet14_LOW5_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet15_LOW5_2 AS LakWasMet15_LOW5_2 ON LakWasMet15_LOW5_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet16_LOW5_2 AS LakWasMet16_LOW5_2 ON LakWasMet16_LOW5_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet19_HOW5_2 AS LakWasMet19_HOW5_2 ON LakWasMet19_HOW5_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet20_HOW5_2 AS LakWasMet20_HOW5_2 ON LakWasMet20_HOW5_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet21_HOW5_2 AS LakWasMet21_HOW5_2 ON LakWasMet21_HOW5_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet22_HOW5_2 AS LakWasMet22_HOW5_2 ON LakWasMet22_HOW5_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet25_LOW6_2 AS LakWasMet25_LOW6_2 ON LakWasMet25_LOW6_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet26_LOW6_2 AS LakWasMet26_LOW6_2 ON LakWasMet26_LOW6_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet27_LOW6_2 AS LakWasMet27_LOW6_2 ON LakWasMet27_LOW6_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet28_LOW6_2 AS LakWasMet28_LOW6_2 ON LakWasMet28_LOW6_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet31_HOW6_2 AS LakWasMet31_HOW6_2 ON LakWasMet31_HOW6_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet32_HOW6_2 AS LakWasMet32_HOW6_2 ON LakWasMet32_HOW6_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet33_HOW6_2 AS LakWasMet33_HOW6_2 ON LakWasMet33_HOW6_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet34_HOW6_2 AS LakWasMet34_HOW6_2 ON LakWasMet34_HOW6_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet37_LOW7_2 AS LakWasMet37_LOW7_2 ON LakWasMet37_LOW7_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet38_LOW7_2 AS LakWasMet38_LOW7_2 ON LakWasMet38_LOW7_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet39_LOW7_2 AS LakWasMet39_LOW7_2 ON LakWasMet39_LOW7_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet40_LOW7_2 AS LakWasMet40_LOW7_2 ON LakWasMet40_LOW7_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet43_HOW7_2 AS LakWasMet43_HOW7_2 ON LakWasMet43_HOW7_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet44_HOW7_2 AS LakWasMet44_HOW7_2 ON LakWasMet44_HOW7_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet45_HOW7_2 AS LakWasMet45_HOW7_2 ON LakWasMet45_HOW7_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet46_HOW7_2 AS LakWasMet46_HOW7_2 ON LakWasMet46_HOW7_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet49_LOW8_2 AS LakWasMet49_LOW8_2 ON LakWasMet49_LOW8_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet50_LOW8_2 AS LakWasMet50_LOW8_2 ON LakWasMet50_LOW8_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet51_LOW8_2 AS LakWasMet51_LOW8_2 ON LakWasMet51_LOW8_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet52_LOW8_2 AS LakWasMet52_LOW8_2 ON LakWasMet52_LOW8_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet55_HOW8_2 AS LakWasMet55_HOW8_2 ON LakWasMet55_HOW8_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet56_HOW8_2 AS LakWasMet56_HOW8_2 ON LakWasMet56_HOW8_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet57_HOW8_2 AS LakWasMet57_HOW8_2 ON LakWasMet57_HOW8_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet58_HOW8_2 AS LakWasMet58_HOW8_2 ON LakWasMet58_HOW8_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet61_LOW9_2 AS LakWasMet61_LOW9_2 ON LakWasMet61_LOW9_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet62_LOW9_2 AS LakWasMet62_LOW9_2 ON LakWasMet62_LOW9_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet63_LOW9_2 AS LakWasMet63_LOW9_2 ON LakWasMet63_LOW9_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet64_LOW9_2 AS LakWasMet64_LOW9_2 ON LakWasMet64_LOW9_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet67_HOW9_2 AS LakWasMet67_HOW9_2 ON LakWasMet67_HOW9_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet68_HOW9_2 AS LakWasMet68_HOW9_2 ON LakWasMet68_HOW9_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet69_HOW9_2 AS LakWasMet69_HOW9_2 ON LakWasMet69_HOW9_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMet70_HOW9_2 AS LakWasMet70_HOW9_2 ON LakWasMet70_HOW9_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMeta1_LOW4_2 AS LakWasMeta1_LOW4_2 ON LakWasMeta1_LOW4_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMeta2_LOW4_2 AS LakWasMeta2_LOW4_2 ON LakWasMeta2_LOW4_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMeta3_LOW4_2 AS LakWasMeta3_LOW4_2 ON LakWasMeta3_LOW4_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMeta4_LOW4_2 AS LakWasMeta4_LOW4_2 ON LakWasMeta4_LOW4_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMeta7_HOW4_2 AS LakWasMeta7_HOW4_2 ON LakWasMeta7_HOW4_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMeta8_HOW4_2 AS LakWasMeta8_HOW4_2 ON LakWasMeta8_HOW4_2.locus_tag = g.locus_tag
		LEFT JOIN summary_LakWasMeta9_HOW4_2 AS LakWasMeta9_HOW4_2 ON LakWasMeta9_HOW4_2.locus_tag = g.locus_tag
WHERE type = 'CDS'
;

SELECT p1.*, p2.* FROM summary_meta4_part1 AS p1 INNER JOIN summary_meta4_part2 AS p2 ON p1.locus_tag = p2.locus_tag;
