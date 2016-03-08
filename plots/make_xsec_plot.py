#!/usr/bin/env python
import sys
import argparse
tmparg = sys.argv[:]
sys.argv = []
import math
import ROOT
import os
from array import array
sys.argv = tmparg

def errorPlotFromFile(file_name):
    xvals = []
    central = []
    errorup = []
    errordown = []
    error2up = []
    error2down = []
    num_lines = 0
    with open(file_name) as input_file:
        for line in input_file:
            num_lines += 1
            values = line.split()
            if len(values) < 2:
                print "Invalid input file %s" % file_name
                exit(0)
            xvals.append(float(values[0]))
            central.append(float(values[1]))
            if len(values) < 3:
                print "No error values found in input file %s" % file_name
                continue
            if "%" in values[2]:
                values[2] = float(values[1])*float(values[2].strip("%"))/100
            if "%" in values[3]:
                values[3] = float(values[1])*float(values[3].strip("%"))/100
            errorup.append(float(values[2]))
            errordown.append(float(values[3]))
            if len(values) == 6:
                error2down.append(math.sqrt(float(values[2])**2 + float(values[4])**2))
                error2up.append(math.sqrt(float(values[3])**2 + float(values[5])**2))
    error_graph = ROOT.TGraphAsymmErrors(num_lines,
        array('f', xvals),
        array('f', central),
        array('f', [0 for val in xvals]), #No x errors
        array('f', [0 for val in xvals]), #No x errors
        array('f', errordown),
        array('f', errorup)
    )
    syst_error_graph = 0
    if len(error2up) != 0:
        syst_error_graph = ROOT.TGraphAsymmErrors(num_lines,
            array('f', xvals),
            array('f', central),
            array('f', [0 for val in xvals]), #No x errors
            array('f', [0 for val in xvals]), #No x errors
            array('f', error2down),
            array('f', error2up)
        )
    return (error_graph, syst_error_graph)
parser = argparse.ArgumentParser()
ROOT.gROOT.SetBatch()
ROOT.dotrootImport('nsmith-/CMSPlotDecorations')
parser.add_argument("analysis", choices=["WZ", "ZZ"])
parser.add_argument("--nodata", action='store_true')
parser.add_argument("--include_lo", action='store_true')

args = parser.parse_args()

mc_file = "data/%s_scan_values_removebr.txt" % args.analysis
#mc_file = "data/%s_MCFM_published_nlo_values.txt" % args.analysis
if not os.path.isfile(mc_file):
    print "Invalid data file %s" % mc_file
    exit(0)

(xsec_graph, pdf_errs) = errorPlotFromFile(mc_file)
xsec_graph.SetLineColor(ROOT.TColor.GetColor("#FFE6EC"))
xsec_graph.SetLineColor(ROOT.TColor.GetColor("#ca0020"))
xsec_graph.SetFillColor(ROOT.TColor.GetColor("#FFE6EC"))
xsec_graph.SetLineWidth(1)
if pdf_errs:
    pdf_errs.SetLineColor(ROOT.TColor.GetColor("#F8D4DA"))
    pdf_errs.SetFillColor(ROOT.TColor.GetColor("#F8D4DA"))

canvas = ROOT.TCanvas("canvas", "canvas", 600, 600)
if not args.nodata:
    (data_graph, sys_errors) = errorPlotFromFile("data/%s_CMS_measurements.txt" % args.analysis)
    data_graph.SetMarkerStyle(20)
    data_graph.SetLineWidth(1)
    data_graph.SetMarkerSize(1)

    sys_errors.SetMarkerStyle(20)
    sys_errors.SetLineWidth(2)
    sys_errors.SetMarkerSize(1)
    #sys_errors.SetMarkerColor(10)
    (atlas_data_graph, atlas_sys_errors) = errorPlotFromFile("data/%s_ATLAS_measurements.txt" % args.analysis)
    atlas_data_graph.SetMarkerStyle(26)
    atlas_data_graph.SetLineWidth(1)
    atlas_data_graph.SetMarkerSize(1)
    atlas_sys_errors.SetMarkerColor(10)
    atlas_sys_errors.SetMarkerStyle(22)
    atlas_sys_errors.SetLineWidth(2)
    atlas_sys_errors.SetMarkerSize(1)
first_plot = pdf_errs if pdf_errs else xsec_graph
first_plot.SetMaximum(23 if args.analysis == "ZZ" else 57)
if args.analysis == "ZZ" or args.include_lo:
    first_plot.SetMinimum(2)

first_plot.Draw("A3")
first_plot.GetXaxis().SetRangeUser(5.6, 14.35)
first_plot.GetXaxis().SetTitle("#sqrt{s} (TeV)")
first_plot.GetYaxis().SetTitle("#sigma_{pp #rightarrow %s}(pb)" % args.analysis)
if pdf_errs:
    xsec_graph.Draw("3")

xsec_graph_clone = xsec_graph.Clone()
xsec_graph_clone.SetLineColor(ROOT.TColor.GetColor("#ca0020"))
xsec_graph_clone.Draw("CX")

if args.analysis == "ZZ":
    nnlo_graph = errorPlotFromFile("data/ZZ_nnlo_values.txt")[0]
    nnlo_graph.SetFillColor(ROOT.TColor.GetColor("#A3DFFF"))
    nnlo_graph.SetLineColor(ROOT.TColor.GetColor("#002D80"))
    nnlo_graph.Draw("3 same")
    nnlo_graph_clone = nnlo_graph.Clone()
    nnlo_graph_clone.SetLineColor(ROOT.TColor.GetColor("#002D80"))
    nnlo_graph_clone.Draw("CX")
    
    mcfm_nlo_graph = errorPlotFromFile("data/ZZ_MCFM_published_nlo_values.txt")[0]
    mcfm_nlo_graph.SetFillColorAlpha(ROOT.TColor.GetColor("#C2FFBD"), 0.4)
    mcfm_nlo_graph.SetLineColor(ROOT.TColor.GetColor("#004D00"))
    mcfm_nlo_graph.Draw("3 same")                               
    mcfm_nlo_graph_clone = mcfm_nlo_graph.Clone()
    mcfm_nlo_graph_clone.SetLineColor(ROOT.TColor.GetColor("#004D00"))
    mcfm_nlo_graph_clone.Draw("CX")

    (zz2l2v_data_graph, zz2l2v_sys_errors) = errorPlotFromFile("data/ZZ2l2v_CMS_measurements.txt")
    zz2l2v_data_graph.SetMarkerStyle(21)
    zz2l2v_data_graph.SetLineWidth(1)
    zz2l2v_data_graph.SetMarkerSize(1)
    zz2l2v_sys_errors.SetMarkerStyle(21)
    zz2l2v_sys_errors.SetLineWidth(2)
    #zz2l2v_sys_errors.SetMarkerColor(10)
    zz2l2v_sys_errors.SetMarkerSize(1)
    zz2l2v_data_graph.Draw("P same")
    zz2l2v_sys_errors.Draw("P same")
if args.include_lo:
    mcfm_lo_graph = errorPlotFromFile("data/%s_MCFM_published_lo_values.txt" % args.analysis)[0]
    mcfm_lo_graph.SetFillColor(ROOT.TColor.GetColor("#A3DFFF"))
    mcfm_lo_graph.SetLineColor(ROOT.TColor.GetColor("#002D80"))
    mcfm_lo_graph.Draw("3 same")                               
    mcfm_lo_graph_clone = mcfm_lo_graph.Clone()
    mcfm_lo_graph_clone.SetLineColor(ROOT.TColor.GetColor("#004D00"))
    mcfm_lo_graph_clone.SetLineColor(ROOT.TColor.GetColor("#002D80"))
    mcfm_lo_graph_clone.Draw("CX")
if not args.nodata:
    data_graph.Draw("P same")
    sys_errors.Draw("P same")
    atlas_data_graph.Draw("P same")
    atlas_sys_errors.Draw("P same")
ROOT.gStyle.SetEndErrorSize(4)
#legend = ROOT.TLegend(0.20, 0.65 - (0.10 if args.analysis == "ZZ" else 0.0), 0.55, 0.85 )
#legend = ROOT.TLegend(*([0.18, 0.55, .53, .90] if args.analysis == "ZZ" else [0.20, 0.65, 0.55, 0.85]))
mc_legend = ROOT.TLegend(*([0.18, 0.55, .53, .78] if args.analysis == "ZZ" else [0.20, 0.71, 0.55, 0.79]))
data_legend = ROOT.TLegend(*([0.18, 0.78, .53, .90] if args.analysis == "ZZ" else [0.20, 0.80, 0.55, 0.90]))
if not args.nodata:
    data_legend.AddEntry(data_graph,
            "CMS %s" % ("" if args.analysis == "WZ" else "4l channel"),
            "p"
    )
if args.analysis == "ZZ":
    data_legend.AddEntry(zz2l2v_data_graph,
            "CMS 2l2#nu channel",
            "p"
    )
if not args.nodata:
    data_legend.AddEntry(atlas_data_graph,
            "ATLAS %s" % ("" if args.analysis == "WZ" else "4l channel"),
            "p"
    )
if args.include_lo:
    mc_legend.AddEntry(mcfm_lo_graph,
            "LO",
            "fl"
    )
if args.analysis == "ZZ":
    mc_legend.AddEntry(nnlo_graph,
            "#splitline{#sigma_{NNLO (qq+qg+gg)} Cascioli et. al.}"
            "{#scale[0.7]{ MMSTW2008, fixed #mu_{F}= #mu_{R}= M_{Z}}}",
            "lf"
    )
    mc_legend.AddEntry(mcfm_nlo_graph,
            "#splitline{#sigma_{NLO+gg} Campbell et. al.}"
            "{#scale[0.7]{ MMSTW2008, fixed #mu_{F}= #mu_{R}= M_{Z}}}",
            "lf"
    )
mc_legend.AddEntry(xsec_graph,
       "#splitline{#sigma_{NLO%s} via MCFM}"
        "{#scale[0.7]{NNPDF3.0, dynamic #mu_{F}= #mu_{R}= M_{%s}}}" % 
            (("+gg", "ZZ") if args.analysis == "ZZ" else ("", "WZ")),
        "lf"
)
mc_legend.Draw()
data_legend.Draw()
ROOT.CMSlumi(canvas,0, 33)
ROOT.gPad.RedrawAxis()

canvas.Print("~/public_html/DibosonPlots/%sCrossSection.pdf" % args.analysis)
