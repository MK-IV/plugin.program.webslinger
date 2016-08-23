<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US">
<head>
<link rel="icon" href="/cpython/static/hgicon.png" type="image/png" />
<meta name="robots" content="index, nofollow" />
<link rel="stylesheet" href="/cpython/static/style-paper.css" type="text/css" />
<script type="text/javascript" src="/cpython/static/mercurial.js"></script>

<link rel="stylesheet" href="/cpython/highlightcss" type="text/css" />
<title>cpython: 75111791110b Lib/webbrowser.py</title>
</head>
<body>

<div class="container">
<div class="menu">
<div class="logo">
<a href="https://hg.python.org">
<img src="/cpython/static/hglogo.png" alt="back to hg.python.org repositories" /></a>
</div>
<ul>
<li><a href="/cpython/shortlog/2.7">log</a></li>
<li><a href="/cpython/graph/2.7">graph</a></li>
<li><a href="/cpython/tags">tags</a></li>
<li><a href="/cpython/bookmarks">bookmarks</a></li>
<li><a href="/cpython/branches">branches</a></li>
</ul>
<ul>
<li><a href="/cpython/rev/2.7">changeset</a></li>
<li><a href="/cpython/file/2.7/Lib/">browse</a></li>
</ul>
<ul>
<li class="active">file</li>
<li><a href="/cpython/file/tip/Lib/webbrowser.py">latest</a></li>
<li><a href="/cpython/diff/2.7/Lib/webbrowser.py">diff</a></li>
<li><a href="/cpython/comparison/2.7/Lib/webbrowser.py">comparison</a></li>
<li><a href="/cpython/annotate/2.7/Lib/webbrowser.py">annotate</a></li>
<li><a href="/cpython/log/2.7/Lib/webbrowser.py">file log</a></li>
<li><a href="/cpython/raw-file/2.7/Lib/webbrowser.py">raw</a></li>
</ul>
<ul>
<li><a href="/cpython/help">help</a></li>
</ul>
</div>

<div class="main">
<h2 class="breadcrumb"><a href="/">Mercurial</a> &gt; <a href="/cpython">cpython</a> </h2>
<h3>
 view Lib/webbrowser.py @ 102858:<a href="/cpython/rev/75111791110b">75111791110b</a>
 <span class="branchname">2.7</span> 
</h3>

<form class="search" action="/cpython/log">

<p><input name="rev" id="search1" type="text" size="30" /></p>
<div id="hint">Find changesets by keywords (author, files, the commit message), revision
number or hash, or <a href="/cpython/help/revsets">revset expression</a>.</div>
</form>

<div class="description"># 2466: ismount now recognizes mount points user can't access.

Patch by Robin Roth, backport by Xiang Zhang.</a> [<a href="http://bugs.python.org/2466" class="issuelink">#2466</a>]</div>

<table id="changesetEntry">
<tr>
 <th class="author">author</th>
 <td class="author">&#82;&#32;&#68;&#97;&#118;&#105;&#100;&#32;&#77;&#117;&#114;&#114;&#97;&#121;&#32;&#60;&#114;&#100;&#109;&#117;&#114;&#114;&#97;&#121;&#64;&#98;&#105;&#116;&#100;&#97;&#110;&#99;&#101;&#46;&#99;&#111;&#109;&#62;</td>
</tr>
<tr>
 <th class="date">date</th>
 <td class="date age">Tue, 23 Aug 2016 12:30:28 -0400</td>
</tr>
<tr>
 <th class="author">parents</th>
 <td class="author"><a href="/cpython/file/5a1429e9b621/Lib/webbrowser.py">5a1429e9b621</a> </td>
</tr>
<tr>
 <th class="author">children</th>
 <td class="author"></td>
</tr>
</table>

<div class="overflow">
<div class="sourcefirst linewraptoggle">line wrap: <a class="linewraplink" href="javascript:toggleLinewrap()">on</a></div>
<div class="sourcefirst"> line source</div>
<pre class="sourcelines stripes4 wrap">
<span id="l1"><span class="c">#! /usr/bin/env python</span></span><a href="#l1"></a>
<span id="l2"><span class="sd">&quot;&quot;&quot;Interfaces for launching and remotely controlling Web browsers.&quot;&quot;&quot;</span></span><a href="#l2"></a>
<span id="l3"><span class="c"># Maintained by Georg Brandl.</span></span><a href="#l3"></a>
<span id="l4"></span><a href="#l4"></a>
<span id="l5"><span class="kn">import</span> <span class="nn">os</span></span><a href="#l5"></a>
<span id="l6"><span class="kn">import</span> <span class="nn">shlex</span></span><a href="#l6"></a>
<span id="l7"><span class="kn">import</span> <span class="nn">sys</span></span><a href="#l7"></a>
<span id="l8"><span class="kn">import</span> <span class="nn">stat</span></span><a href="#l8"></a>
<span id="l9"><span class="kn">import</span> <span class="nn">subprocess</span></span><a href="#l9"></a>
<span id="l10"><span class="kn">import</span> <span class="nn">time</span></span><a href="#l10"></a>
<span id="l11"></span><a href="#l11"></a>
<span id="l12"><span class="n">__all__</span> <span class="o">=</span> <span class="p">[</span><span class="s">&quot;Error&quot;</span><span class="p">,</span> <span class="s">&quot;open&quot;</span><span class="p">,</span> <span class="s">&quot;open_new&quot;</span><span class="p">,</span> <span class="s">&quot;open_new_tab&quot;</span><span class="p">,</span> <span class="s">&quot;get&quot;</span><span class="p">,</span> <span class="s">&quot;register&quot;</span><span class="p">]</span></span><a href="#l12"></a>
<span id="l13"></span><a href="#l13"></a>
<span id="l14"><span class="k">class</span> <span class="nc">Error</span><span class="p">(</span><span class="ne">Exception</span><span class="p">):</span></span><a href="#l14"></a>
<span id="l15">    <span class="k">pass</span></span><a href="#l15"></a>
<span id="l16"></span><a href="#l16"></a>
<span id="l17"><span class="n">_browsers</span> <span class="o">=</span> <span class="p">{}</span>          <span class="c"># Dictionary of available browser controllers</span></span><a href="#l17"></a>
<span id="l18"><span class="n">_tryorder</span> <span class="o">=</span> <span class="p">[]</span>          <span class="c"># Preference order of available browsers</span></span><a href="#l18"></a>
<span id="l19"></span><a href="#l19"></a>
<span id="l20"><span class="k">def</span> <span class="nf">register</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="n">klass</span><span class="p">,</span> <span class="n">instance</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="n">update_tryorder</span><span class="o">=</span><span class="mi">1</span><span class="p">):</span></span><a href="#l20"></a>
<span id="l21">    <span class="sd">&quot;&quot;&quot;Register a browser connector and, optionally, connection.&quot;&quot;&quot;</span></span><a href="#l21"></a>
<span id="l22">    <span class="n">_browsers</span><span class="p">[</span><span class="n">name</span><span class="o">.</span><span class="n">lower</span><span class="p">()]</span> <span class="o">=</span> <span class="p">[</span><span class="n">klass</span><span class="p">,</span> <span class="n">instance</span><span class="p">]</span></span><a href="#l22"></a>
<span id="l23">    <span class="k">if</span> <span class="n">update_tryorder</span> <span class="o">&gt;</span> <span class="mi">0</span><span class="p">:</span></span><a href="#l23"></a>
<span id="l24">        <span class="n">_tryorder</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">name</span><span class="p">)</span></span><a href="#l24"></a>
<span id="l25">    <span class="k">elif</span> <span class="n">update_tryorder</span> <span class="o">&lt;</span> <span class="mi">0</span><span class="p">:</span></span><a href="#l25"></a>
<span id="l26">        <span class="n">_tryorder</span><span class="o">.</span><span class="n">insert</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">name</span><span class="p">)</span></span><a href="#l26"></a>
<span id="l27"></span><a href="#l27"></a>
<span id="l28"><span class="k">def</span> <span class="nf">get</span><span class="p">(</span><span class="n">using</span><span class="o">=</span><span class="bp">None</span><span class="p">):</span></span><a href="#l28"></a>
<span id="l29">    <span class="sd">&quot;&quot;&quot;Return a browser launcher instance appropriate for the environment.&quot;&quot;&quot;</span></span><a href="#l29"></a>
<span id="l30">    <span class="k">if</span> <span class="n">using</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l30"></a>
<span id="l31">        <span class="n">alternatives</span> <span class="o">=</span> <span class="p">[</span><span class="n">using</span><span class="p">]</span></span><a href="#l31"></a>
<span id="l32">    <span class="k">else</span><span class="p">:</span></span><a href="#l32"></a>
<span id="l33">        <span class="n">alternatives</span> <span class="o">=</span> <span class="n">_tryorder</span></span><a href="#l33"></a>
<span id="l34">    <span class="k">for</span> <span class="n">browser</span> <span class="ow">in</span> <span class="n">alternatives</span><span class="p">:</span></span><a href="#l34"></a>
<span id="l35">        <span class="k">if</span> <span class="s">&#39;</span><span class="si">%s</span><span class="s">&#39;</span> <span class="ow">in</span> <span class="n">browser</span><span class="p">:</span></span><a href="#l35"></a>
<span id="l36">            <span class="c"># User gave us a command line, split it into name and args</span></span><a href="#l36"></a>
<span id="l37">            <span class="n">browser</span> <span class="o">=</span> <span class="n">shlex</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="n">browser</span><span class="p">)</span></span><a href="#l37"></a>
<span id="l38">            <span class="k">if</span> <span class="n">browser</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="o">==</span> <span class="s">&#39;&amp;&#39;</span><span class="p">:</span></span><a href="#l38"></a>
<span id="l39">                <span class="k">return</span> <span class="n">BackgroundBrowser</span><span class="p">(</span><span class="n">browser</span><span class="p">[:</span><span class="o">-</span><span class="mi">1</span><span class="p">])</span></span><a href="#l39"></a>
<span id="l40">            <span class="k">else</span><span class="p">:</span></span><a href="#l40"></a>
<span id="l41">                <span class="k">return</span> <span class="n">GenericBrowser</span><span class="p">(</span><span class="n">browser</span><span class="p">)</span></span><a href="#l41"></a>
<span id="l42">        <span class="k">else</span><span class="p">:</span></span><a href="#l42"></a>
<span id="l43">            <span class="c"># User gave us a browser name or path.</span></span><a href="#l43"></a>
<span id="l44">            <span class="k">try</span><span class="p">:</span></span><a href="#l44"></a>
<span id="l45">                <span class="n">command</span> <span class="o">=</span> <span class="n">_browsers</span><span class="p">[</span><span class="n">browser</span><span class="o">.</span><span class="n">lower</span><span class="p">()]</span></span><a href="#l45"></a>
<span id="l46">            <span class="k">except</span> <span class="ne">KeyError</span><span class="p">:</span></span><a href="#l46"></a>
<span id="l47">                <span class="n">command</span> <span class="o">=</span> <span class="n">_synthesize</span><span class="p">(</span><span class="n">browser</span><span class="p">)</span></span><a href="#l47"></a>
<span id="l48">            <span class="k">if</span> <span class="n">command</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l48"></a>
<span id="l49">                <span class="k">return</span> <span class="n">command</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span></span><a href="#l49"></a>
<span id="l50">            <span class="k">elif</span> <span class="n">command</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l50"></a>
<span id="l51">                <span class="k">return</span> <span class="n">command</span><span class="p">[</span><span class="mi">0</span><span class="p">]()</span></span><a href="#l51"></a>
<span id="l52">    <span class="k">raise</span> <span class="n">Error</span><span class="p">(</span><span class="s">&quot;could not locate runnable browser&quot;</span><span class="p">)</span></span><a href="#l52"></a>
<span id="l53"></span><a href="#l53"></a>
<span id="l54"><span class="c"># Please note: the following definition hides a builtin function.</span></span><a href="#l54"></a>
<span id="l55"><span class="c"># It is recommended one does &quot;import webbrowser&quot; and uses webbrowser.open(url)</span></span><a href="#l55"></a>
<span id="l56"><span class="c"># instead of &quot;from webbrowser import *&quot;.</span></span><a href="#l56"></a>
<span id="l57"></span><a href="#l57"></a>
<span id="l58"><span class="k">def</span> <span class="nf">open</span><span class="p">(</span><span class="n">url</span><span class="p">,</span> <span class="n">new</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">autoraise</span><span class="o">=</span><span class="bp">True</span><span class="p">):</span></span><a href="#l58"></a>
<span id="l59">    <span class="k">for</span> <span class="n">name</span> <span class="ow">in</span> <span class="n">_tryorder</span><span class="p">:</span></span><a href="#l59"></a>
<span id="l60">        <span class="n">browser</span> <span class="o">=</span> <span class="n">get</span><span class="p">(</span><span class="n">name</span><span class="p">)</span></span><a href="#l60"></a>
<span id="l61">        <span class="k">if</span> <span class="n">browser</span><span class="o">.</span><span class="n">open</span><span class="p">(</span><span class="n">url</span><span class="p">,</span> <span class="n">new</span><span class="p">,</span> <span class="n">autoraise</span><span class="p">):</span></span><a href="#l61"></a>
<span id="l62">            <span class="k">return</span> <span class="bp">True</span></span><a href="#l62"></a>
<span id="l63">    <span class="k">return</span> <span class="bp">False</span></span><a href="#l63"></a>
<span id="l64"></span><a href="#l64"></a>
<span id="l65"><span class="k">def</span> <span class="nf">open_new</span><span class="p">(</span><span class="n">url</span><span class="p">):</span></span><a href="#l65"></a>
<span id="l66">    <span class="k">return</span> <span class="nb">open</span><span class="p">(</span><span class="n">url</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span></span><a href="#l66"></a>
<span id="l67"></span><a href="#l67"></a>
<span id="l68"><span class="k">def</span> <span class="nf">open_new_tab</span><span class="p">(</span><span class="n">url</span><span class="p">):</span></span><a href="#l68"></a>
<span id="l69">    <span class="k">return</span> <span class="nb">open</span><span class="p">(</span><span class="n">url</span><span class="p">,</span> <span class="mi">2</span><span class="p">)</span></span><a href="#l69"></a>
<span id="l70"></span><a href="#l70"></a>
<span id="l71"></span><a href="#l71"></a>
<span id="l72"><span class="k">def</span> <span class="nf">_synthesize</span><span class="p">(</span><span class="n">browser</span><span class="p">,</span> <span class="n">update_tryorder</span><span class="o">=</span><span class="mi">1</span><span class="p">):</span></span><a href="#l72"></a>
<span id="l73">    <span class="sd">&quot;&quot;&quot;Attempt to synthesize a controller base on existing controllers.</span></span><a href="#l73"></a>
<span id="l74"></span><a href="#l74"></a>
<span id="l75"><span class="sd">    This is useful to create a controller when a user specifies a path to</span></span><a href="#l75"></a>
<span id="l76"><span class="sd">    an entry in the BROWSER environment variable -- we can copy a general</span></span><a href="#l76"></a>
<span id="l77"><span class="sd">    controller to operate using a specific installation of the desired</span></span><a href="#l77"></a>
<span id="l78"><span class="sd">    browser in this way.</span></span><a href="#l78"></a>
<span id="l79"></span><a href="#l79"></a>
<span id="l80"><span class="sd">    If we can&#39;t create a controller in this way, or if there is no</span></span><a href="#l80"></a>
<span id="l81"><span class="sd">    executable for the requested browser, return [None, None].</span></span><a href="#l81"></a>
<span id="l82"></span><a href="#l82"></a>
<span id="l83"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l83"></a>
<span id="l84">    <span class="n">cmd</span> <span class="o">=</span> <span class="n">browser</span><span class="o">.</span><span class="n">split</span><span class="p">()[</span><span class="mi">0</span><span class="p">]</span></span><a href="#l84"></a>
<span id="l85">    <span class="k">if</span> <span class="ow">not</span> <span class="n">_iscommand</span><span class="p">(</span><span class="n">cmd</span><span class="p">):</span></span><a href="#l85"></a>
<span id="l86">        <span class="k">return</span> <span class="p">[</span><span class="bp">None</span><span class="p">,</span> <span class="bp">None</span><span class="p">]</span></span><a href="#l86"></a>
<span id="l87">    <span class="n">name</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">basename</span><span class="p">(</span><span class="n">cmd</span><span class="p">)</span></span><a href="#l87"></a>
<span id="l88">    <span class="k">try</span><span class="p">:</span></span><a href="#l88"></a>
<span id="l89">        <span class="n">command</span> <span class="o">=</span> <span class="n">_browsers</span><span class="p">[</span><span class="n">name</span><span class="o">.</span><span class="n">lower</span><span class="p">()]</span></span><a href="#l89"></a>
<span id="l90">    <span class="k">except</span> <span class="ne">KeyError</span><span class="p">:</span></span><a href="#l90"></a>
<span id="l91">        <span class="k">return</span> <span class="p">[</span><span class="bp">None</span><span class="p">,</span> <span class="bp">None</span><span class="p">]</span></span><a href="#l91"></a>
<span id="l92">    <span class="c"># now attempt to clone to fit the new name:</span></span><a href="#l92"></a>
<span id="l93">    <span class="n">controller</span> <span class="o">=</span> <span class="n">command</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span></span><a href="#l93"></a>
<span id="l94">    <span class="k">if</span> <span class="n">controller</span> <span class="ow">and</span> <span class="n">name</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span> <span class="o">==</span> <span class="n">controller</span><span class="o">.</span><span class="n">basename</span><span class="p">:</span></span><a href="#l94"></a>
<span id="l95">        <span class="kn">import</span> <span class="nn">copy</span></span><a href="#l95"></a>
<span id="l96">        <span class="n">controller</span> <span class="o">=</span> <span class="n">copy</span><span class="o">.</span><span class="n">copy</span><span class="p">(</span><span class="n">controller</span><span class="p">)</span></span><a href="#l96"></a>
<span id="l97">        <span class="n">controller</span><span class="o">.</span><span class="n">name</span> <span class="o">=</span> <span class="n">browser</span></span><a href="#l97"></a>
<span id="l98">        <span class="n">controller</span><span class="o">.</span><span class="n">basename</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">basename</span><span class="p">(</span><span class="n">browser</span><span class="p">)</span></span><a href="#l98"></a>
<span id="l99">        <span class="n">register</span><span class="p">(</span><span class="n">browser</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">controller</span><span class="p">,</span> <span class="n">update_tryorder</span><span class="p">)</span></span><a href="#l99"></a>
<span id="l100">        <span class="k">return</span> <span class="p">[</span><span class="bp">None</span><span class="p">,</span> <span class="n">controller</span><span class="p">]</span></span><a href="#l100"></a>
<span id="l101">    <span class="k">return</span> <span class="p">[</span><span class="bp">None</span><span class="p">,</span> <span class="bp">None</span><span class="p">]</span></span><a href="#l101"></a>
<span id="l102"></span><a href="#l102"></a>
<span id="l103"></span><a href="#l103"></a>
<span id="l104"><span class="k">if</span> <span class="n">sys</span><span class="o">.</span><span class="n">platform</span><span class="p">[:</span><span class="mi">3</span><span class="p">]</span> <span class="o">==</span> <span class="s">&quot;win&quot;</span><span class="p">:</span></span><a href="#l104"></a>
<span id="l105">    <span class="k">def</span> <span class="nf">_isexecutable</span><span class="p">(</span><span class="n">cmd</span><span class="p">):</span></span><a href="#l105"></a>
<span id="l106">        <span class="n">cmd</span> <span class="o">=</span> <span class="n">cmd</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span></span><a href="#l106"></a>
<span id="l107">        <span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">isfile</span><span class="p">(</span><span class="n">cmd</span><span class="p">)</span> <span class="ow">and</span> <span class="n">cmd</span><span class="o">.</span><span class="n">endswith</span><span class="p">((</span><span class="s">&quot;.exe&quot;</span><span class="p">,</span> <span class="s">&quot;.bat&quot;</span><span class="p">)):</span></span><a href="#l107"></a>
<span id="l108">            <span class="k">return</span> <span class="bp">True</span></span><a href="#l108"></a>
<span id="l109">        <span class="k">for</span> <span class="n">ext</span> <span class="ow">in</span> <span class="s">&quot;.exe&quot;</span><span class="p">,</span> <span class="s">&quot;.bat&quot;</span><span class="p">:</span></span><a href="#l109"></a>
<span id="l110">            <span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">isfile</span><span class="p">(</span><span class="n">cmd</span> <span class="o">+</span> <span class="n">ext</span><span class="p">):</span></span><a href="#l110"></a>
<span id="l111">                <span class="k">return</span> <span class="bp">True</span></span><a href="#l111"></a>
<span id="l112">        <span class="k">return</span> <span class="bp">False</span></span><a href="#l112"></a>
<span id="l113"><span class="k">else</span><span class="p">:</span></span><a href="#l113"></a>
<span id="l114">    <span class="k">def</span> <span class="nf">_isexecutable</span><span class="p">(</span><span class="n">cmd</span><span class="p">):</span></span><a href="#l114"></a>
<span id="l115">        <span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">isfile</span><span class="p">(</span><span class="n">cmd</span><span class="p">):</span></span><a href="#l115"></a>
<span id="l116">            <span class="n">mode</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">stat</span><span class="p">(</span><span class="n">cmd</span><span class="p">)[</span><span class="n">stat</span><span class="o">.</span><span class="n">ST_MODE</span><span class="p">]</span></span><a href="#l116"></a>
<span id="l117">            <span class="k">if</span> <span class="n">mode</span> <span class="o">&amp;</span> <span class="n">stat</span><span class="o">.</span><span class="n">S_IXUSR</span> <span class="ow">or</span> <span class="n">mode</span> <span class="o">&amp;</span> <span class="n">stat</span><span class="o">.</span><span class="n">S_IXGRP</span> <span class="ow">or</span> <span class="n">mode</span> <span class="o">&amp;</span> <span class="n">stat</span><span class="o">.</span><span class="n">S_IXOTH</span><span class="p">:</span></span><a href="#l117"></a>
<span id="l118">                <span class="k">return</span> <span class="bp">True</span></span><a href="#l118"></a>
<span id="l119">        <span class="k">return</span> <span class="bp">False</span></span><a href="#l119"></a>
<span id="l120"></span><a href="#l120"></a>
<span id="l121"><span class="k">def</span> <span class="nf">_iscommand</span><span class="p">(</span><span class="n">cmd</span><span class="p">):</span></span><a href="#l121"></a>
<span id="l122">    <span class="sd">&quot;&quot;&quot;Return True if cmd is executable or can be found on the executable</span></span><a href="#l122"></a>
<span id="l123"><span class="sd">    search path.&quot;&quot;&quot;</span></span><a href="#l123"></a>
<span id="l124">    <span class="k">if</span> <span class="n">_isexecutable</span><span class="p">(</span><span class="n">cmd</span><span class="p">):</span></span><a href="#l124"></a>
<span id="l125">        <span class="k">return</span> <span class="bp">True</span></span><a href="#l125"></a>
<span id="l126">    <span class="n">path</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&quot;PATH&quot;</span><span class="p">)</span></span><a href="#l126"></a>
<span id="l127">    <span class="k">if</span> <span class="ow">not</span> <span class="n">path</span><span class="p">:</span></span><a href="#l127"></a>
<span id="l128">        <span class="k">return</span> <span class="bp">False</span></span><a href="#l128"></a>
<span id="l129">    <span class="k">for</span> <span class="n">d</span> <span class="ow">in</span> <span class="n">path</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">pathsep</span><span class="p">):</span></span><a href="#l129"></a>
<span id="l130">        <span class="n">exe</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">d</span><span class="p">,</span> <span class="n">cmd</span><span class="p">)</span></span><a href="#l130"></a>
<span id="l131">        <span class="k">if</span> <span class="n">_isexecutable</span><span class="p">(</span><span class="n">exe</span><span class="p">):</span></span><a href="#l131"></a>
<span id="l132">            <span class="k">return</span> <span class="bp">True</span></span><a href="#l132"></a>
<span id="l133">    <span class="k">return</span> <span class="bp">False</span></span><a href="#l133"></a>
<span id="l134"></span><a href="#l134"></a>
<span id="l135"></span><a href="#l135"></a>
<span id="l136"><span class="c"># General parent classes</span></span><a href="#l136"></a>
<span id="l137"></span><a href="#l137"></a>
<span id="l138"><span class="k">class</span> <span class="nc">BaseBrowser</span><span class="p">(</span><span class="nb">object</span><span class="p">):</span></span><a href="#l138"></a>
<span id="l139">    <span class="sd">&quot;&quot;&quot;Parent class for all browsers. Do not use directly.&quot;&quot;&quot;</span></span><a href="#l139"></a>
<span id="l140"></span><a href="#l140"></a>
<span id="l141">    <span class="n">args</span> <span class="o">=</span> <span class="p">[</span><span class="s">&#39;</span><span class="si">%s</span><span class="s">&#39;</span><span class="p">]</span></span><a href="#l141"></a>
<span id="l142"></span><a href="#l142"></a>
<span id="l143">    <span class="k">def</span> <span class="nf">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="o">=</span><span class="s">&quot;&quot;</span><span class="p">):</span></span><a href="#l143"></a>
<span id="l144">        <span class="bp">self</span><span class="o">.</span><span class="n">name</span> <span class="o">=</span> <span class="n">name</span></span><a href="#l144"></a>
<span id="l145">        <span class="bp">self</span><span class="o">.</span><span class="n">basename</span> <span class="o">=</span> <span class="n">name</span></span><a href="#l145"></a>
<span id="l146"></span><a href="#l146"></a>
<span id="l147">    <span class="k">def</span> <span class="nf">open</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">url</span><span class="p">,</span> <span class="n">new</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">autoraise</span><span class="o">=</span><span class="bp">True</span><span class="p">):</span></span><a href="#l147"></a>
<span id="l148">        <span class="k">raise</span> <span class="ne">NotImplementedError</span></span><a href="#l148"></a>
<span id="l149"></span><a href="#l149"></a>
<span id="l150">    <span class="k">def</span> <span class="nf">open_new</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">url</span><span class="p">):</span></span><a href="#l150"></a>
<span id="l151">        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">open</span><span class="p">(</span><span class="n">url</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span></span><a href="#l151"></a>
<span id="l152"></span><a href="#l152"></a>
<span id="l153">    <span class="k">def</span> <span class="nf">open_new_tab</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">url</span><span class="p">):</span></span><a href="#l153"></a>
<span id="l154">        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">open</span><span class="p">(</span><span class="n">url</span><span class="p">,</span> <span class="mi">2</span><span class="p">)</span></span><a href="#l154"></a>
<span id="l155"></span><a href="#l155"></a>
<span id="l156"></span><a href="#l156"></a>
<span id="l157"><span class="k">class</span> <span class="nc">GenericBrowser</span><span class="p">(</span><span class="n">BaseBrowser</span><span class="p">):</span></span><a href="#l157"></a>
<span id="l158">    <span class="sd">&quot;&quot;&quot;Class for all browsers started with a command</span></span><a href="#l158"></a>
<span id="l159"><span class="sd">       and without remote functionality.&quot;&quot;&quot;</span></span><a href="#l159"></a>
<span id="l160"></span><a href="#l160"></a>
<span id="l161">    <span class="k">def</span> <span class="nf">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">):</span></span><a href="#l161"></a>
<span id="l162">        <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="nb">basestring</span><span class="p">):</span></span><a href="#l162"></a>
<span id="l163">            <span class="bp">self</span><span class="o">.</span><span class="n">name</span> <span class="o">=</span> <span class="n">name</span></span><a href="#l163"></a>
<span id="l164">            <span class="bp">self</span><span class="o">.</span><span class="n">args</span> <span class="o">=</span> <span class="p">[</span><span class="s">&quot;</span><span class="si">%s</span><span class="s">&quot;</span><span class="p">]</span></span><a href="#l164"></a>
<span id="l165">        <span class="k">else</span><span class="p">:</span></span><a href="#l165"></a>
<span id="l166">            <span class="c"># name should be a list with arguments</span></span><a href="#l166"></a>
<span id="l167">            <span class="bp">self</span><span class="o">.</span><span class="n">name</span> <span class="o">=</span> <span class="n">name</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span></span><a href="#l167"></a>
<span id="l168">            <span class="bp">self</span><span class="o">.</span><span class="n">args</span> <span class="o">=</span> <span class="n">name</span><span class="p">[</span><span class="mi">1</span><span class="p">:]</span></span><a href="#l168"></a>
<span id="l169">        <span class="bp">self</span><span class="o">.</span><span class="n">basename</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">basename</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">name</span><span class="p">)</span></span><a href="#l169"></a>
<span id="l170"></span><a href="#l170"></a>
<span id="l171">    <span class="k">def</span> <span class="nf">open</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">url</span><span class="p">,</span> <span class="n">new</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">autoraise</span><span class="o">=</span><span class="bp">True</span><span class="p">):</span></span><a href="#l171"></a>
<span id="l172">        <span class="n">cmdline</span> <span class="o">=</span> <span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">name</span><span class="p">]</span> <span class="o">+</span> <span class="p">[</span><span class="n">arg</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="s">&quot;</span><span class="si">%s</span><span class="s">&quot;</span><span class="p">,</span> <span class="n">url</span><span class="p">)</span></span><a href="#l172"></a>
<span id="l173">                                 <span class="k">for</span> <span class="n">arg</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">args</span><span class="p">]</span></span><a href="#l173"></a>
<span id="l174">        <span class="k">try</span><span class="p">:</span></span><a href="#l174"></a>
<span id="l175">            <span class="k">if</span> <span class="n">sys</span><span class="o">.</span><span class="n">platform</span><span class="p">[:</span><span class="mi">3</span><span class="p">]</span> <span class="o">==</span> <span class="s">&#39;win&#39;</span><span class="p">:</span></span><a href="#l175"></a>
<span id="l176">                <span class="n">p</span> <span class="o">=</span> <span class="n">subprocess</span><span class="o">.</span><span class="n">Popen</span><span class="p">(</span><span class="n">cmdline</span><span class="p">)</span></span><a href="#l176"></a>
<span id="l177">            <span class="k">else</span><span class="p">:</span></span><a href="#l177"></a>
<span id="l178">                <span class="n">p</span> <span class="o">=</span> <span class="n">subprocess</span><span class="o">.</span><span class="n">Popen</span><span class="p">(</span><span class="n">cmdline</span><span class="p">,</span> <span class="n">close_fds</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span></span><a href="#l178"></a>
<span id="l179">            <span class="k">return</span> <span class="ow">not</span> <span class="n">p</span><span class="o">.</span><span class="n">wait</span><span class="p">()</span></span><a href="#l179"></a>
<span id="l180">        <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l180"></a>
<span id="l181">            <span class="k">return</span> <span class="bp">False</span></span><a href="#l181"></a>
<span id="l182"></span><a href="#l182"></a>
<span id="l183"></span><a href="#l183"></a>
<span id="l184"><span class="k">class</span> <span class="nc">BackgroundBrowser</span><span class="p">(</span><span class="n">GenericBrowser</span><span class="p">):</span></span><a href="#l184"></a>
<span id="l185">    <span class="sd">&quot;&quot;&quot;Class for all browsers which are to be started in the</span></span><a href="#l185"></a>
<span id="l186"><span class="sd">       background.&quot;&quot;&quot;</span></span><a href="#l186"></a>
<span id="l187"></span><a href="#l187"></a>
<span id="l188">    <span class="k">def</span> <span class="nf">open</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">url</span><span class="p">,</span> <span class="n">new</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">autoraise</span><span class="o">=</span><span class="bp">True</span><span class="p">):</span></span><a href="#l188"></a>
<span id="l189">        <span class="n">cmdline</span> <span class="o">=</span> <span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">name</span><span class="p">]</span> <span class="o">+</span> <span class="p">[</span><span class="n">arg</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="s">&quot;</span><span class="si">%s</span><span class="s">&quot;</span><span class="p">,</span> <span class="n">url</span><span class="p">)</span></span><a href="#l189"></a>
<span id="l190">                                 <span class="k">for</span> <span class="n">arg</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">args</span><span class="p">]</span></span><a href="#l190"></a>
<span id="l191">        <span class="k">try</span><span class="p">:</span></span><a href="#l191"></a>
<span id="l192">            <span class="k">if</span> <span class="n">sys</span><span class="o">.</span><span class="n">platform</span><span class="p">[:</span><span class="mi">3</span><span class="p">]</span> <span class="o">==</span> <span class="s">&#39;win&#39;</span><span class="p">:</span></span><a href="#l192"></a>
<span id="l193">                <span class="n">p</span> <span class="o">=</span> <span class="n">subprocess</span><span class="o">.</span><span class="n">Popen</span><span class="p">(</span><span class="n">cmdline</span><span class="p">)</span></span><a href="#l193"></a>
<span id="l194">            <span class="k">else</span><span class="p">:</span></span><a href="#l194"></a>
<span id="l195">                <span class="n">setsid</span> <span class="o">=</span> <span class="nb">getattr</span><span class="p">(</span><span class="n">os</span><span class="p">,</span> <span class="s">&#39;setsid&#39;</span><span class="p">,</span> <span class="bp">None</span><span class="p">)</span></span><a href="#l195"></a>
<span id="l196">                <span class="k">if</span> <span class="ow">not</span> <span class="n">setsid</span><span class="p">:</span></span><a href="#l196"></a>
<span id="l197">                    <span class="n">setsid</span> <span class="o">=</span> <span class="nb">getattr</span><span class="p">(</span><span class="n">os</span><span class="p">,</span> <span class="s">&#39;setpgrp&#39;</span><span class="p">,</span> <span class="bp">None</span><span class="p">)</span></span><a href="#l197"></a>
<span id="l198">                <span class="n">p</span> <span class="o">=</span> <span class="n">subprocess</span><span class="o">.</span><span class="n">Popen</span><span class="p">(</span><span class="n">cmdline</span><span class="p">,</span> <span class="n">close_fds</span><span class="o">=</span><span class="bp">True</span><span class="p">,</span> <span class="n">preexec_fn</span><span class="o">=</span><span class="n">setsid</span><span class="p">)</span></span><a href="#l198"></a>
<span id="l199">            <span class="k">return</span> <span class="p">(</span><span class="n">p</span><span class="o">.</span><span class="n">poll</span><span class="p">()</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">)</span></span><a href="#l199"></a>
<span id="l200">        <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l200"></a>
<span id="l201">            <span class="k">return</span> <span class="bp">False</span></span><a href="#l201"></a>
<span id="l202"></span><a href="#l202"></a>
<span id="l203"></span><a href="#l203"></a>
<span id="l204"><span class="k">class</span> <span class="nc">UnixBrowser</span><span class="p">(</span><span class="n">BaseBrowser</span><span class="p">):</span></span><a href="#l204"></a>
<span id="l205">    <span class="sd">&quot;&quot;&quot;Parent class for all Unix browsers with remote functionality.&quot;&quot;&quot;</span></span><a href="#l205"></a>
<span id="l206"></span><a href="#l206"></a>
<span id="l207">    <span class="n">raise_opts</span> <span class="o">=</span> <span class="bp">None</span></span><a href="#l207"></a>
<span id="l208">    <span class="n">remote_args</span> <span class="o">=</span> <span class="p">[</span><span class="s">&#39;%action&#39;</span><span class="p">,</span> <span class="s">&#39;</span><span class="si">%s</span><span class="s">&#39;</span><span class="p">]</span></span><a href="#l208"></a>
<span id="l209">    <span class="n">remote_action</span> <span class="o">=</span> <span class="bp">None</span></span><a href="#l209"></a>
<span id="l210">    <span class="n">remote_action_newwin</span> <span class="o">=</span> <span class="bp">None</span></span><a href="#l210"></a>
<span id="l211">    <span class="n">remote_action_newtab</span> <span class="o">=</span> <span class="bp">None</span></span><a href="#l211"></a>
<span id="l212">    <span class="n">background</span> <span class="o">=</span> <span class="bp">False</span></span><a href="#l212"></a>
<span id="l213">    <span class="n">redirect_stdout</span> <span class="o">=</span> <span class="bp">True</span></span><a href="#l213"></a>
<span id="l214"></span><a href="#l214"></a>
<span id="l215">    <span class="k">def</span> <span class="nf">_invoke</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">args</span><span class="p">,</span> <span class="n">remote</span><span class="p">,</span> <span class="n">autoraise</span><span class="p">):</span></span><a href="#l215"></a>
<span id="l216">        <span class="n">raise_opt</span> <span class="o">=</span> <span class="p">[]</span></span><a href="#l216"></a>
<span id="l217">        <span class="k">if</span> <span class="n">remote</span> <span class="ow">and</span> <span class="bp">self</span><span class="o">.</span><span class="n">raise_opts</span><span class="p">:</span></span><a href="#l217"></a>
<span id="l218">            <span class="c"># use autoraise argument only for remote invocation</span></span><a href="#l218"></a>
<span id="l219">            <span class="n">autoraise</span> <span class="o">=</span> <span class="nb">int</span><span class="p">(</span><span class="n">autoraise</span><span class="p">)</span></span><a href="#l219"></a>
<span id="l220">            <span class="n">opt</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">raise_opts</span><span class="p">[</span><span class="n">autoraise</span><span class="p">]</span></span><a href="#l220"></a>
<span id="l221">            <span class="k">if</span> <span class="n">opt</span><span class="p">:</span> <span class="n">raise_opt</span> <span class="o">=</span> <span class="p">[</span><span class="n">opt</span><span class="p">]</span></span><a href="#l221"></a>
<span id="l222"></span><a href="#l222"></a>
<span id="l223">        <span class="n">cmdline</span> <span class="o">=</span> <span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">name</span><span class="p">]</span> <span class="o">+</span> <span class="n">raise_opt</span> <span class="o">+</span> <span class="n">args</span></span><a href="#l223"></a>
<span id="l224"></span><a href="#l224"></a>
<span id="l225">        <span class="k">if</span> <span class="n">remote</span> <span class="ow">or</span> <span class="bp">self</span><span class="o">.</span><span class="n">background</span><span class="p">:</span></span><a href="#l225"></a>
<span id="l226">            <span class="n">inout</span> <span class="o">=</span> <span class="nb">file</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">devnull</span><span class="p">,</span> <span class="s">&quot;r+&quot;</span><span class="p">)</span></span><a href="#l226"></a>
<span id="l227">        <span class="k">else</span><span class="p">:</span></span><a href="#l227"></a>
<span id="l228">            <span class="c"># for TTY browsers, we need stdin/out</span></span><a href="#l228"></a>
<span id="l229">            <span class="n">inout</span> <span class="o">=</span> <span class="bp">None</span></span><a href="#l229"></a>
<span id="l230">        <span class="c"># if possible, put browser in separate process group, so</span></span><a href="#l230"></a>
<span id="l231">        <span class="c"># keyboard interrupts don&#39;t affect browser as well as Python</span></span><a href="#l231"></a>
<span id="l232">        <span class="n">setsid</span> <span class="o">=</span> <span class="nb">getattr</span><span class="p">(</span><span class="n">os</span><span class="p">,</span> <span class="s">&#39;setsid&#39;</span><span class="p">,</span> <span class="bp">None</span><span class="p">)</span></span><a href="#l232"></a>
<span id="l233">        <span class="k">if</span> <span class="ow">not</span> <span class="n">setsid</span><span class="p">:</span></span><a href="#l233"></a>
<span id="l234">            <span class="n">setsid</span> <span class="o">=</span> <span class="nb">getattr</span><span class="p">(</span><span class="n">os</span><span class="p">,</span> <span class="s">&#39;setpgrp&#39;</span><span class="p">,</span> <span class="bp">None</span><span class="p">)</span></span><a href="#l234"></a>
<span id="l235"></span><a href="#l235"></a>
<span id="l236">        <span class="n">p</span> <span class="o">=</span> <span class="n">subprocess</span><span class="o">.</span><span class="n">Popen</span><span class="p">(</span><span class="n">cmdline</span><span class="p">,</span> <span class="n">close_fds</span><span class="o">=</span><span class="bp">True</span><span class="p">,</span> <span class="n">stdin</span><span class="o">=</span><span class="n">inout</span><span class="p">,</span></span><a href="#l236"></a>
<span id="l237">                             <span class="n">stdout</span><span class="o">=</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">redirect_stdout</span> <span class="ow">and</span> <span class="n">inout</span> <span class="ow">or</span> <span class="bp">None</span><span class="p">),</span></span><a href="#l237"></a>
<span id="l238">                             <span class="n">stderr</span><span class="o">=</span><span class="n">inout</span><span class="p">,</span> <span class="n">preexec_fn</span><span class="o">=</span><span class="n">setsid</span><span class="p">)</span></span><a href="#l238"></a>
<span id="l239">        <span class="k">if</span> <span class="n">remote</span><span class="p">:</span></span><a href="#l239"></a>
<span id="l240">            <span class="c"># wait five seconds. If the subprocess is not finished, the</span></span><a href="#l240"></a>
<span id="l241">            <span class="c"># remote invocation has (hopefully) started a new instance.</span></span><a href="#l241"></a>
<span id="l242">            <span class="n">time</span><span class="o">.</span><span class="n">sleep</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span></span><a href="#l242"></a>
<span id="l243">            <span class="n">rc</span> <span class="o">=</span> <span class="n">p</span><span class="o">.</span><span class="n">poll</span><span class="p">()</span></span><a href="#l243"></a>
<span id="l244">            <span class="k">if</span> <span class="n">rc</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l244"></a>
<span id="l245">                <span class="n">time</span><span class="o">.</span><span class="n">sleep</span><span class="p">(</span><span class="mi">4</span><span class="p">)</span></span><a href="#l245"></a>
<span id="l246">                <span class="n">rc</span> <span class="o">=</span> <span class="n">p</span><span class="o">.</span><span class="n">poll</span><span class="p">()</span></span><a href="#l246"></a>
<span id="l247">                <span class="k">if</span> <span class="n">rc</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l247"></a>
<span id="l248">                    <span class="k">return</span> <span class="bp">True</span></span><a href="#l248"></a>
<span id="l249">            <span class="c"># if remote call failed, open() will try direct invocation</span></span><a href="#l249"></a>
<span id="l250">            <span class="k">return</span> <span class="ow">not</span> <span class="n">rc</span></span><a href="#l250"></a>
<span id="l251">        <span class="k">elif</span> <span class="bp">self</span><span class="o">.</span><span class="n">background</span><span class="p">:</span></span><a href="#l251"></a>
<span id="l252">            <span class="k">if</span> <span class="n">p</span><span class="o">.</span><span class="n">poll</span><span class="p">()</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l252"></a>
<span id="l253">                <span class="k">return</span> <span class="bp">True</span></span><a href="#l253"></a>
<span id="l254">            <span class="k">else</span><span class="p">:</span></span><a href="#l254"></a>
<span id="l255">                <span class="k">return</span> <span class="bp">False</span></span><a href="#l255"></a>
<span id="l256">        <span class="k">else</span><span class="p">:</span></span><a href="#l256"></a>
<span id="l257">            <span class="k">return</span> <span class="ow">not</span> <span class="n">p</span><span class="o">.</span><span class="n">wait</span><span class="p">()</span></span><a href="#l257"></a>
<span id="l258"></span><a href="#l258"></a>
<span id="l259">    <span class="k">def</span> <span class="nf">open</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">url</span><span class="p">,</span> <span class="n">new</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">autoraise</span><span class="o">=</span><span class="bp">True</span><span class="p">):</span></span><a href="#l259"></a>
<span id="l260">        <span class="k">if</span> <span class="n">new</span> <span class="o">==</span> <span class="mi">0</span><span class="p">:</span></span><a href="#l260"></a>
<span id="l261">            <span class="n">action</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">remote_action</span></span><a href="#l261"></a>
<span id="l262">        <span class="k">elif</span> <span class="n">new</span> <span class="o">==</span> <span class="mi">1</span><span class="p">:</span></span><a href="#l262"></a>
<span id="l263">            <span class="n">action</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">remote_action_newwin</span></span><a href="#l263"></a>
<span id="l264">        <span class="k">elif</span> <span class="n">new</span> <span class="o">==</span> <span class="mi">2</span><span class="p">:</span></span><a href="#l264"></a>
<span id="l265">            <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">remote_action_newtab</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l265"></a>
<span id="l266">                <span class="n">action</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">remote_action_newwin</span></span><a href="#l266"></a>
<span id="l267">            <span class="k">else</span><span class="p">:</span></span><a href="#l267"></a>
<span id="l268">                <span class="n">action</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">remote_action_newtab</span></span><a href="#l268"></a>
<span id="l269">        <span class="k">else</span><span class="p">:</span></span><a href="#l269"></a>
<span id="l270">            <span class="k">raise</span> <span class="n">Error</span><span class="p">(</span><span class="s">&quot;Bad &#39;new&#39; parameter to open(); &quot;</span> <span class="o">+</span></span><a href="#l270"></a>
<span id="l271">                        <span class="s">&quot;expected 0, 1, or 2, got </span><span class="si">%s</span><span class="s">&quot;</span> <span class="o">%</span> <span class="n">new</span><span class="p">)</span></span><a href="#l271"></a>
<span id="l272"></span><a href="#l272"></a>
<span id="l273">        <span class="n">args</span> <span class="o">=</span> <span class="p">[</span><span class="n">arg</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="s">&quot;</span><span class="si">%s</span><span class="s">&quot;</span><span class="p">,</span> <span class="n">url</span><span class="p">)</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="s">&quot;%action&quot;</span><span class="p">,</span> <span class="n">action</span><span class="p">)</span></span><a href="#l273"></a>
<span id="l274">                <span class="k">for</span> <span class="n">arg</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">remote_args</span><span class="p">]</span></span><a href="#l274"></a>
<span id="l275">        <span class="n">success</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_invoke</span><span class="p">(</span><span class="n">args</span><span class="p">,</span> <span class="bp">True</span><span class="p">,</span> <span class="n">autoraise</span><span class="p">)</span></span><a href="#l275"></a>
<span id="l276">        <span class="k">if</span> <span class="ow">not</span> <span class="n">success</span><span class="p">:</span></span><a href="#l276"></a>
<span id="l277">            <span class="c"># remote invocation failed, try straight way</span></span><a href="#l277"></a>
<span id="l278">            <span class="n">args</span> <span class="o">=</span> <span class="p">[</span><span class="n">arg</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="s">&quot;</span><span class="si">%s</span><span class="s">&quot;</span><span class="p">,</span> <span class="n">url</span><span class="p">)</span> <span class="k">for</span> <span class="n">arg</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">args</span><span class="p">]</span></span><a href="#l278"></a>
<span id="l279">            <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_invoke</span><span class="p">(</span><span class="n">args</span><span class="p">,</span> <span class="bp">False</span><span class="p">,</span> <span class="bp">False</span><span class="p">)</span></span><a href="#l279"></a>
<span id="l280">        <span class="k">else</span><span class="p">:</span></span><a href="#l280"></a>
<span id="l281">            <span class="k">return</span> <span class="bp">True</span></span><a href="#l281"></a>
<span id="l282"></span><a href="#l282"></a>
<span id="l283"></span><a href="#l283"></a>
<span id="l284"><span class="k">class</span> <span class="nc">Mozilla</span><span class="p">(</span><span class="n">UnixBrowser</span><span class="p">):</span></span><a href="#l284"></a>
<span id="l285">    <span class="sd">&quot;&quot;&quot;Launcher class for Mozilla/Netscape browsers.&quot;&quot;&quot;</span></span><a href="#l285"></a>
<span id="l286"></span><a href="#l286"></a>
<span id="l287">    <span class="n">raise_opts</span> <span class="o">=</span> <span class="p">[</span><span class="s">&quot;-noraise&quot;</span><span class="p">,</span> <span class="s">&quot;-raise&quot;</span><span class="p">]</span></span><a href="#l287"></a>
<span id="l288">    <span class="n">remote_args</span> <span class="o">=</span> <span class="p">[</span><span class="s">&#39;-remote&#39;</span><span class="p">,</span> <span class="s">&#39;openURL(</span><span class="si">%s</span><span class="s">%action)&#39;</span><span class="p">]</span></span><a href="#l288"></a>
<span id="l289">    <span class="n">remote_action</span> <span class="o">=</span> <span class="s">&quot;&quot;</span></span><a href="#l289"></a>
<span id="l290">    <span class="n">remote_action_newwin</span> <span class="o">=</span> <span class="s">&quot;,new-window&quot;</span></span><a href="#l290"></a>
<span id="l291">    <span class="n">remote_action_newtab</span> <span class="o">=</span> <span class="s">&quot;,new-tab&quot;</span></span><a href="#l291"></a>
<span id="l292">    <span class="n">background</span> <span class="o">=</span> <span class="bp">True</span></span><a href="#l292"></a>
<span id="l293"></span><a href="#l293"></a>
<span id="l294"><span class="n">Netscape</span> <span class="o">=</span> <span class="n">Mozilla</span></span><a href="#l294"></a>
<span id="l295"></span><a href="#l295"></a>
<span id="l296"></span><a href="#l296"></a>
<span id="l297"><span class="k">class</span> <span class="nc">Galeon</span><span class="p">(</span><span class="n">UnixBrowser</span><span class="p">):</span></span><a href="#l297"></a>
<span id="l298">    <span class="sd">&quot;&quot;&quot;Launcher class for Galeon/Epiphany browsers.&quot;&quot;&quot;</span></span><a href="#l298"></a>
<span id="l299"></span><a href="#l299"></a>
<span id="l300">    <span class="n">raise_opts</span> <span class="o">=</span> <span class="p">[</span><span class="s">&quot;-noraise&quot;</span><span class="p">,</span> <span class="s">&quot;&quot;</span><span class="p">]</span></span><a href="#l300"></a>
<span id="l301">    <span class="n">remote_args</span> <span class="o">=</span> <span class="p">[</span><span class="s">&#39;%action&#39;</span><span class="p">,</span> <span class="s">&#39;</span><span class="si">%s</span><span class="s">&#39;</span><span class="p">]</span></span><a href="#l301"></a>
<span id="l302">    <span class="n">remote_action</span> <span class="o">=</span> <span class="s">&quot;-n&quot;</span></span><a href="#l302"></a>
<span id="l303">    <span class="n">remote_action_newwin</span> <span class="o">=</span> <span class="s">&quot;-w&quot;</span></span><a href="#l303"></a>
<span id="l304">    <span class="n">background</span> <span class="o">=</span> <span class="bp">True</span></span><a href="#l304"></a>
<span id="l305"></span><a href="#l305"></a>
<span id="l306"></span><a href="#l306"></a>
<span id="l307"><span class="k">class</span> <span class="nc">Chrome</span><span class="p">(</span><span class="n">UnixBrowser</span><span class="p">):</span></span><a href="#l307"></a>
<span id="l308">    <span class="s">&quot;Launcher class for Google Chrome browser.&quot;</span></span><a href="#l308"></a>
<span id="l309"></span><a href="#l309"></a>
<span id="l310">    <span class="n">remote_args</span> <span class="o">=</span> <span class="p">[</span><span class="s">&#39;%action&#39;</span><span class="p">,</span> <span class="s">&#39;</span><span class="si">%s</span><span class="s">&#39;</span><span class="p">]</span></span><a href="#l310"></a>
<span id="l311">    <span class="n">remote_action</span> <span class="o">=</span> <span class="s">&quot;&quot;</span></span><a href="#l311"></a>
<span id="l312">    <span class="n">remote_action_newwin</span> <span class="o">=</span> <span class="s">&quot;--new-window&quot;</span></span><a href="#l312"></a>
<span id="l313">    <span class="n">remote_action_newtab</span> <span class="o">=</span> <span class="s">&quot;&quot;</span></span><a href="#l313"></a>
<span id="l314">    <span class="n">background</span> <span class="o">=</span> <span class="bp">True</span></span><a href="#l314"></a>
<span id="l315"></span><a href="#l315"></a>
<span id="l316"><span class="n">Chromium</span> <span class="o">=</span> <span class="n">Chrome</span></span><a href="#l316"></a>
<span id="l317"></span><a href="#l317"></a>
<span id="l318"></span><a href="#l318"></a>
<span id="l319"><span class="k">class</span> <span class="nc">Opera</span><span class="p">(</span><span class="n">UnixBrowser</span><span class="p">):</span></span><a href="#l319"></a>
<span id="l320">    <span class="s">&quot;Launcher class for Opera browser.&quot;</span></span><a href="#l320"></a>
<span id="l321"></span><a href="#l321"></a>
<span id="l322">    <span class="n">raise_opts</span> <span class="o">=</span> <span class="p">[</span><span class="s">&quot;-noraise&quot;</span><span class="p">,</span> <span class="s">&quot;&quot;</span><span class="p">]</span></span><a href="#l322"></a>
<span id="l323">    <span class="n">remote_args</span> <span class="o">=</span> <span class="p">[</span><span class="s">&#39;-remote&#39;</span><span class="p">,</span> <span class="s">&#39;openURL(</span><span class="si">%s</span><span class="s">%action)&#39;</span><span class="p">]</span></span><a href="#l323"></a>
<span id="l324">    <span class="n">remote_action</span> <span class="o">=</span> <span class="s">&quot;&quot;</span></span><a href="#l324"></a>
<span id="l325">    <span class="n">remote_action_newwin</span> <span class="o">=</span> <span class="s">&quot;,new-window&quot;</span></span><a href="#l325"></a>
<span id="l326">    <span class="n">remote_action_newtab</span> <span class="o">=</span> <span class="s">&quot;,new-page&quot;</span></span><a href="#l326"></a>
<span id="l327">    <span class="n">background</span> <span class="o">=</span> <span class="bp">True</span></span><a href="#l327"></a>
<span id="l328"></span><a href="#l328"></a>
<span id="l329"></span><a href="#l329"></a>
<span id="l330"><span class="k">class</span> <span class="nc">Elinks</span><span class="p">(</span><span class="n">UnixBrowser</span><span class="p">):</span></span><a href="#l330"></a>
<span id="l331">    <span class="s">&quot;Launcher class for Elinks browsers.&quot;</span></span><a href="#l331"></a>
<span id="l332"></span><a href="#l332"></a>
<span id="l333">    <span class="n">remote_args</span> <span class="o">=</span> <span class="p">[</span><span class="s">&#39;-remote&#39;</span><span class="p">,</span> <span class="s">&#39;openURL(</span><span class="si">%s</span><span class="s">%action)&#39;</span><span class="p">]</span></span><a href="#l333"></a>
<span id="l334">    <span class="n">remote_action</span> <span class="o">=</span> <span class="s">&quot;&quot;</span></span><a href="#l334"></a>
<span id="l335">    <span class="n">remote_action_newwin</span> <span class="o">=</span> <span class="s">&quot;,new-window&quot;</span></span><a href="#l335"></a>
<span id="l336">    <span class="n">remote_action_newtab</span> <span class="o">=</span> <span class="s">&quot;,new-tab&quot;</span></span><a href="#l336"></a>
<span id="l337">    <span class="n">background</span> <span class="o">=</span> <span class="bp">False</span></span><a href="#l337"></a>
<span id="l338"></span><a href="#l338"></a>
<span id="l339">    <span class="c"># elinks doesn&#39;t like its stdout to be redirected -</span></span><a href="#l339"></a>
<span id="l340">    <span class="c"># it uses redirected stdout as a signal to do -dump</span></span><a href="#l340"></a>
<span id="l341">    <span class="n">redirect_stdout</span> <span class="o">=</span> <span class="bp">False</span></span><a href="#l341"></a>
<span id="l342"></span><a href="#l342"></a>
<span id="l343"></span><a href="#l343"></a>
<span id="l344"><span class="k">class</span> <span class="nc">Konqueror</span><span class="p">(</span><span class="n">BaseBrowser</span><span class="p">):</span></span><a href="#l344"></a>
<span id="l345">    <span class="sd">&quot;&quot;&quot;Controller for the KDE File Manager (kfm, or Konqueror).</span></span><a href="#l345"></a>
<span id="l346"></span><a href="#l346"></a>
<span id="l347"><span class="sd">    See the output of ``kfmclient --commands``</span></span><a href="#l347"></a>
<span id="l348"><span class="sd">    for more information on the Konqueror remote-control interface.</span></span><a href="#l348"></a>
<span id="l349"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l349"></a>
<span id="l350"></span><a href="#l350"></a>
<span id="l351">    <span class="k">def</span> <span class="nf">open</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">url</span><span class="p">,</span> <span class="n">new</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">autoraise</span><span class="o">=</span><span class="bp">True</span><span class="p">):</span></span><a href="#l351"></a>
<span id="l352">        <span class="c"># XXX Currently I know no way to prevent KFM from opening a new win.</span></span><a href="#l352"></a>
<span id="l353">        <span class="k">if</span> <span class="n">new</span> <span class="o">==</span> <span class="mi">2</span><span class="p">:</span></span><a href="#l353"></a>
<span id="l354">            <span class="n">action</span> <span class="o">=</span> <span class="s">&quot;newTab&quot;</span></span><a href="#l354"></a>
<span id="l355">        <span class="k">else</span><span class="p">:</span></span><a href="#l355"></a>
<span id="l356">            <span class="n">action</span> <span class="o">=</span> <span class="s">&quot;openURL&quot;</span></span><a href="#l356"></a>
<span id="l357"></span><a href="#l357"></a>
<span id="l358">        <span class="n">devnull</span> <span class="o">=</span> <span class="nb">file</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">devnull</span><span class="p">,</span> <span class="s">&quot;r+&quot;</span><span class="p">)</span></span><a href="#l358"></a>
<span id="l359">        <span class="c"># if possible, put browser in separate process group, so</span></span><a href="#l359"></a>
<span id="l360">        <span class="c"># keyboard interrupts don&#39;t affect browser as well as Python</span></span><a href="#l360"></a>
<span id="l361">        <span class="n">setsid</span> <span class="o">=</span> <span class="nb">getattr</span><span class="p">(</span><span class="n">os</span><span class="p">,</span> <span class="s">&#39;setsid&#39;</span><span class="p">,</span> <span class="bp">None</span><span class="p">)</span></span><a href="#l361"></a>
<span id="l362">        <span class="k">if</span> <span class="ow">not</span> <span class="n">setsid</span><span class="p">:</span></span><a href="#l362"></a>
<span id="l363">            <span class="n">setsid</span> <span class="o">=</span> <span class="nb">getattr</span><span class="p">(</span><span class="n">os</span><span class="p">,</span> <span class="s">&#39;setpgrp&#39;</span><span class="p">,</span> <span class="bp">None</span><span class="p">)</span></span><a href="#l363"></a>
<span id="l364"></span><a href="#l364"></a>
<span id="l365">        <span class="k">try</span><span class="p">:</span></span><a href="#l365"></a>
<span id="l366">            <span class="n">p</span> <span class="o">=</span> <span class="n">subprocess</span><span class="o">.</span><span class="n">Popen</span><span class="p">([</span><span class="s">&quot;kfmclient&quot;</span><span class="p">,</span> <span class="n">action</span><span class="p">,</span> <span class="n">url</span><span class="p">],</span></span><a href="#l366"></a>
<span id="l367">                                 <span class="n">close_fds</span><span class="o">=</span><span class="bp">True</span><span class="p">,</span> <span class="n">stdin</span><span class="o">=</span><span class="n">devnull</span><span class="p">,</span></span><a href="#l367"></a>
<span id="l368">                                 <span class="n">stdout</span><span class="o">=</span><span class="n">devnull</span><span class="p">,</span> <span class="n">stderr</span><span class="o">=</span><span class="n">devnull</span><span class="p">)</span></span><a href="#l368"></a>
<span id="l369">        <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l369"></a>
<span id="l370">            <span class="c"># fall through to next variant</span></span><a href="#l370"></a>
<span id="l371">            <span class="k">pass</span></span><a href="#l371"></a>
<span id="l372">        <span class="k">else</span><span class="p">:</span></span><a href="#l372"></a>
<span id="l373">            <span class="n">p</span><span class="o">.</span><span class="n">wait</span><span class="p">()</span></span><a href="#l373"></a>
<span id="l374">            <span class="c"># kfmclient&#39;s return code unfortunately has no meaning as it seems</span></span><a href="#l374"></a>
<span id="l375">            <span class="k">return</span> <span class="bp">True</span></span><a href="#l375"></a>
<span id="l376"></span><a href="#l376"></a>
<span id="l377">        <span class="k">try</span><span class="p">:</span></span><a href="#l377"></a>
<span id="l378">            <span class="n">p</span> <span class="o">=</span> <span class="n">subprocess</span><span class="o">.</span><span class="n">Popen</span><span class="p">([</span><span class="s">&quot;konqueror&quot;</span><span class="p">,</span> <span class="s">&quot;--silent&quot;</span><span class="p">,</span> <span class="n">url</span><span class="p">],</span></span><a href="#l378"></a>
<span id="l379">                                 <span class="n">close_fds</span><span class="o">=</span><span class="bp">True</span><span class="p">,</span> <span class="n">stdin</span><span class="o">=</span><span class="n">devnull</span><span class="p">,</span></span><a href="#l379"></a>
<span id="l380">                                 <span class="n">stdout</span><span class="o">=</span><span class="n">devnull</span><span class="p">,</span> <span class="n">stderr</span><span class="o">=</span><span class="n">devnull</span><span class="p">,</span></span><a href="#l380"></a>
<span id="l381">                                 <span class="n">preexec_fn</span><span class="o">=</span><span class="n">setsid</span><span class="p">)</span></span><a href="#l381"></a>
<span id="l382">        <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l382"></a>
<span id="l383">            <span class="c"># fall through to next variant</span></span><a href="#l383"></a>
<span id="l384">            <span class="k">pass</span></span><a href="#l384"></a>
<span id="l385">        <span class="k">else</span><span class="p">:</span></span><a href="#l385"></a>
<span id="l386">            <span class="k">if</span> <span class="n">p</span><span class="o">.</span><span class="n">poll</span><span class="p">()</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l386"></a>
<span id="l387">                <span class="c"># Should be running now.</span></span><a href="#l387"></a>
<span id="l388">                <span class="k">return</span> <span class="bp">True</span></span><a href="#l388"></a>
<span id="l389"></span><a href="#l389"></a>
<span id="l390">        <span class="k">try</span><span class="p">:</span></span><a href="#l390"></a>
<span id="l391">            <span class="n">p</span> <span class="o">=</span> <span class="n">subprocess</span><span class="o">.</span><span class="n">Popen</span><span class="p">([</span><span class="s">&quot;kfm&quot;</span><span class="p">,</span> <span class="s">&quot;-d&quot;</span><span class="p">,</span> <span class="n">url</span><span class="p">],</span></span><a href="#l391"></a>
<span id="l392">                                 <span class="n">close_fds</span><span class="o">=</span><span class="bp">True</span><span class="p">,</span> <span class="n">stdin</span><span class="o">=</span><span class="n">devnull</span><span class="p">,</span></span><a href="#l392"></a>
<span id="l393">                                 <span class="n">stdout</span><span class="o">=</span><span class="n">devnull</span><span class="p">,</span> <span class="n">stderr</span><span class="o">=</span><span class="n">devnull</span><span class="p">,</span></span><a href="#l393"></a>
<span id="l394">                                 <span class="n">preexec_fn</span><span class="o">=</span><span class="n">setsid</span><span class="p">)</span></span><a href="#l394"></a>
<span id="l395">        <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l395"></a>
<span id="l396">            <span class="k">return</span> <span class="bp">False</span></span><a href="#l396"></a>
<span id="l397">        <span class="k">else</span><span class="p">:</span></span><a href="#l397"></a>
<span id="l398">            <span class="k">return</span> <span class="p">(</span><span class="n">p</span><span class="o">.</span><span class="n">poll</span><span class="p">()</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">)</span></span><a href="#l398"></a>
<span id="l399"></span><a href="#l399"></a>
<span id="l400"></span><a href="#l400"></a>
<span id="l401"><span class="k">class</span> <span class="nc">Grail</span><span class="p">(</span><span class="n">BaseBrowser</span><span class="p">):</span></span><a href="#l401"></a>
<span id="l402">    <span class="c"># There should be a way to maintain a connection to Grail, but the</span></span><a href="#l402"></a>
<span id="l403">    <span class="c"># Grail remote control protocol doesn&#39;t really allow that at this</span></span><a href="#l403"></a>
<span id="l404">    <span class="c"># point.  It probably never will!</span></span><a href="#l404"></a>
<span id="l405">    <span class="k">def</span> <span class="nf">_find_grail_rc</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></span><a href="#l405"></a>
<span id="l406">        <span class="kn">import</span> <span class="nn">glob</span></span><a href="#l406"></a>
<span id="l407">        <span class="kn">import</span> <span class="nn">pwd</span></span><a href="#l407"></a>
<span id="l408">        <span class="kn">import</span> <span class="nn">socket</span></span><a href="#l408"></a>
<span id="l409">        <span class="kn">import</span> <span class="nn">tempfile</span></span><a href="#l409"></a>
<span id="l410">        <span class="n">tempdir</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">tempfile</span><span class="o">.</span><span class="n">gettempdir</span><span class="p">(),</span></span><a href="#l410"></a>
<span id="l411">                               <span class="s">&quot;.grail-unix&quot;</span><span class="p">)</span></span><a href="#l411"></a>
<span id="l412">        <span class="n">user</span> <span class="o">=</span> <span class="n">pwd</span><span class="o">.</span><span class="n">getpwuid</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">getuid</span><span class="p">())[</span><span class="mi">0</span><span class="p">]</span></span><a href="#l412"></a>
<span id="l413">        <span class="n">filename</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">tempdir</span><span class="p">,</span> <span class="n">user</span> <span class="o">+</span> <span class="s">&quot;-*&quot;</span><span class="p">)</span></span><a href="#l413"></a>
<span id="l414">        <span class="n">maybes</span> <span class="o">=</span> <span class="n">glob</span><span class="o">.</span><span class="n">glob</span><span class="p">(</span><span class="n">filename</span><span class="p">)</span></span><a href="#l414"></a>
<span id="l415">        <span class="k">if</span> <span class="ow">not</span> <span class="n">maybes</span><span class="p">:</span></span><a href="#l415"></a>
<span id="l416">            <span class="k">return</span> <span class="bp">None</span></span><a href="#l416"></a>
<span id="l417">        <span class="n">s</span> <span class="o">=</span> <span class="n">socket</span><span class="o">.</span><span class="n">socket</span><span class="p">(</span><span class="n">socket</span><span class="o">.</span><span class="n">AF_UNIX</span><span class="p">,</span> <span class="n">socket</span><span class="o">.</span><span class="n">SOCK_STREAM</span><span class="p">)</span></span><a href="#l417"></a>
<span id="l418">        <span class="k">for</span> <span class="n">fn</span> <span class="ow">in</span> <span class="n">maybes</span><span class="p">:</span></span><a href="#l418"></a>
<span id="l419">            <span class="c"># need to PING each one until we find one that&#39;s live</span></span><a href="#l419"></a>
<span id="l420">            <span class="k">try</span><span class="p">:</span></span><a href="#l420"></a>
<span id="l421">                <span class="n">s</span><span class="o">.</span><span class="n">connect</span><span class="p">(</span><span class="n">fn</span><span class="p">)</span></span><a href="#l421"></a>
<span id="l422">            <span class="k">except</span> <span class="n">socket</span><span class="o">.</span><span class="n">error</span><span class="p">:</span></span><a href="#l422"></a>
<span id="l423">                <span class="c"># no good; attempt to clean it out, but don&#39;t fail:</span></span><a href="#l423"></a>
<span id="l424">                <span class="k">try</span><span class="p">:</span></span><a href="#l424"></a>
<span id="l425">                    <span class="n">os</span><span class="o">.</span><span class="n">unlink</span><span class="p">(</span><span class="n">fn</span><span class="p">)</span></span><a href="#l425"></a>
<span id="l426">                <span class="k">except</span> <span class="ne">IOError</span><span class="p">:</span></span><a href="#l426"></a>
<span id="l427">                    <span class="k">pass</span></span><a href="#l427"></a>
<span id="l428">            <span class="k">else</span><span class="p">:</span></span><a href="#l428"></a>
<span id="l429">                <span class="k">return</span> <span class="n">s</span></span><a href="#l429"></a>
<span id="l430"></span><a href="#l430"></a>
<span id="l431">    <span class="k">def</span> <span class="nf">_remote</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">action</span><span class="p">):</span></span><a href="#l431"></a>
<span id="l432">        <span class="n">s</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_find_grail_rc</span><span class="p">()</span></span><a href="#l432"></a>
<span id="l433">        <span class="k">if</span> <span class="ow">not</span> <span class="n">s</span><span class="p">:</span></span><a href="#l433"></a>
<span id="l434">            <span class="k">return</span> <span class="mi">0</span></span><a href="#l434"></a>
<span id="l435">        <span class="n">s</span><span class="o">.</span><span class="n">send</span><span class="p">(</span><span class="n">action</span><span class="p">)</span></span><a href="#l435"></a>
<span id="l436">        <span class="n">s</span><span class="o">.</span><span class="n">close</span><span class="p">()</span></span><a href="#l436"></a>
<span id="l437">        <span class="k">return</span> <span class="mi">1</span></span><a href="#l437"></a>
<span id="l438"></span><a href="#l438"></a>
<span id="l439">    <span class="k">def</span> <span class="nf">open</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">url</span><span class="p">,</span> <span class="n">new</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">autoraise</span><span class="o">=</span><span class="bp">True</span><span class="p">):</span></span><a href="#l439"></a>
<span id="l440">        <span class="k">if</span> <span class="n">new</span><span class="p">:</span></span><a href="#l440"></a>
<span id="l441">            <span class="n">ok</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_remote</span><span class="p">(</span><span class="s">&quot;LOADNEW &quot;</span> <span class="o">+</span> <span class="n">url</span><span class="p">)</span></span><a href="#l441"></a>
<span id="l442">        <span class="k">else</span><span class="p">:</span></span><a href="#l442"></a>
<span id="l443">            <span class="n">ok</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_remote</span><span class="p">(</span><span class="s">&quot;LOAD &quot;</span> <span class="o">+</span> <span class="n">url</span><span class="p">)</span></span><a href="#l443"></a>
<span id="l444">        <span class="k">return</span> <span class="n">ok</span></span><a href="#l444"></a>
<span id="l445"></span><a href="#l445"></a>
<span id="l446"></span><a href="#l446"></a>
<span id="l447"><span class="c">#</span></span><a href="#l447"></a>
<span id="l448"><span class="c"># Platform support for Unix</span></span><a href="#l448"></a>
<span id="l449"><span class="c">#</span></span><a href="#l449"></a>
<span id="l450"></span><a href="#l450"></a>
<span id="l451"><span class="c"># These are the right tests because all these Unix browsers require either</span></span><a href="#l451"></a>
<span id="l452"><span class="c"># a console terminal or an X display to run.</span></span><a href="#l452"></a>
<span id="l453"></span><a href="#l453"></a>
<span id="l454"><span class="k">def</span> <span class="nf">register_X_browsers</span><span class="p">():</span></span><a href="#l454"></a>
<span id="l455"></span><a href="#l455"></a>
<span id="l456">    <span class="c"># use xdg-open if around</span></span><a href="#l456"></a>
<span id="l457">    <span class="k">if</span> <span class="n">_iscommand</span><span class="p">(</span><span class="s">&quot;xdg-open&quot;</span><span class="p">):</span></span><a href="#l457"></a>
<span id="l458">        <span class="n">register</span><span class="p">(</span><span class="s">&quot;xdg-open&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">BackgroundBrowser</span><span class="p">(</span><span class="s">&quot;xdg-open&quot;</span><span class="p">))</span></span><a href="#l458"></a>
<span id="l459"></span><a href="#l459"></a>
<span id="l460">    <span class="c"># The default GNOME3 browser</span></span><a href="#l460"></a>
<span id="l461">    <span class="k">if</span> <span class="s">&quot;GNOME_DESKTOP_SESSION_ID&quot;</span> <span class="ow">in</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span> <span class="ow">and</span> <span class="n">_iscommand</span><span class="p">(</span><span class="s">&quot;gvfs-open&quot;</span><span class="p">):</span></span><a href="#l461"></a>
<span id="l462">        <span class="n">register</span><span class="p">(</span><span class="s">&quot;gvfs-open&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">BackgroundBrowser</span><span class="p">(</span><span class="s">&quot;gvfs-open&quot;</span><span class="p">))</span></span><a href="#l462"></a>
<span id="l463"></span><a href="#l463"></a>
<span id="l464">    <span class="c"># The default GNOME browser</span></span><a href="#l464"></a>
<span id="l465">    <span class="k">if</span> <span class="s">&quot;GNOME_DESKTOP_SESSION_ID&quot;</span> <span class="ow">in</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span> <span class="ow">and</span> <span class="n">_iscommand</span><span class="p">(</span><span class="s">&quot;gnome-open&quot;</span><span class="p">):</span></span><a href="#l465"></a>
<span id="l466">        <span class="n">register</span><span class="p">(</span><span class="s">&quot;gnome-open&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">BackgroundBrowser</span><span class="p">(</span><span class="s">&quot;gnome-open&quot;</span><span class="p">))</span></span><a href="#l466"></a>
<span id="l467"></span><a href="#l467"></a>
<span id="l468">    <span class="c"># The default KDE browser</span></span><a href="#l468"></a>
<span id="l469">    <span class="k">if</span> <span class="s">&quot;KDE_FULL_SESSION&quot;</span> <span class="ow">in</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span> <span class="ow">and</span> <span class="n">_iscommand</span><span class="p">(</span><span class="s">&quot;kfmclient&quot;</span><span class="p">):</span></span><a href="#l469"></a>
<span id="l470">        <span class="n">register</span><span class="p">(</span><span class="s">&quot;kfmclient&quot;</span><span class="p">,</span> <span class="n">Konqueror</span><span class="p">,</span> <span class="n">Konqueror</span><span class="p">(</span><span class="s">&quot;kfmclient&quot;</span><span class="p">))</span></span><a href="#l470"></a>
<span id="l471"></span><a href="#l471"></a>
<span id="l472">    <span class="k">if</span> <span class="n">_iscommand</span><span class="p">(</span><span class="s">&quot;x-www-browser&quot;</span><span class="p">):</span></span><a href="#l472"></a>
<span id="l473">        <span class="n">register</span><span class="p">(</span><span class="s">&quot;x-www-browser&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">BackgroundBrowser</span><span class="p">(</span><span class="s">&quot;x-www-browser&quot;</span><span class="p">))</span></span><a href="#l473"></a>
<span id="l474"></span><a href="#l474"></a>
<span id="l475">    <span class="c"># The Mozilla/Netscape browsers</span></span><a href="#l475"></a>
<span id="l476">    <span class="k">for</span> <span class="n">browser</span> <span class="ow">in</span> <span class="p">(</span><span class="s">&quot;mozilla-firefox&quot;</span><span class="p">,</span> <span class="s">&quot;firefox&quot;</span><span class="p">,</span></span><a href="#l476"></a>
<span id="l477">                    <span class="s">&quot;mozilla-firebird&quot;</span><span class="p">,</span> <span class="s">&quot;firebird&quot;</span><span class="p">,</span></span><a href="#l477"></a>
<span id="l478">                    <span class="s">&quot;iceweasel&quot;</span><span class="p">,</span> <span class="s">&quot;iceape&quot;</span><span class="p">,</span></span><a href="#l478"></a>
<span id="l479">                    <span class="s">&quot;seamonkey&quot;</span><span class="p">,</span> <span class="s">&quot;mozilla&quot;</span><span class="p">,</span> <span class="s">&quot;netscape&quot;</span><span class="p">):</span></span><a href="#l479"></a>
<span id="l480">        <span class="k">if</span> <span class="n">_iscommand</span><span class="p">(</span><span class="n">browser</span><span class="p">):</span></span><a href="#l480"></a>
<span id="l481">            <span class="n">register</span><span class="p">(</span><span class="n">browser</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">Mozilla</span><span class="p">(</span><span class="n">browser</span><span class="p">))</span></span><a href="#l481"></a>
<span id="l482"></span><a href="#l482"></a>
<span id="l483">    <span class="c"># Konqueror/kfm, the KDE browser.</span></span><a href="#l483"></a>
<span id="l484">    <span class="k">if</span> <span class="n">_iscommand</span><span class="p">(</span><span class="s">&quot;kfm&quot;</span><span class="p">):</span></span><a href="#l484"></a>
<span id="l485">        <span class="n">register</span><span class="p">(</span><span class="s">&quot;kfm&quot;</span><span class="p">,</span> <span class="n">Konqueror</span><span class="p">,</span> <span class="n">Konqueror</span><span class="p">(</span><span class="s">&quot;kfm&quot;</span><span class="p">))</span></span><a href="#l485"></a>
<span id="l486">    <span class="k">elif</span> <span class="n">_iscommand</span><span class="p">(</span><span class="s">&quot;konqueror&quot;</span><span class="p">):</span></span><a href="#l486"></a>
<span id="l487">        <span class="n">register</span><span class="p">(</span><span class="s">&quot;konqueror&quot;</span><span class="p">,</span> <span class="n">Konqueror</span><span class="p">,</span> <span class="n">Konqueror</span><span class="p">(</span><span class="s">&quot;konqueror&quot;</span><span class="p">))</span></span><a href="#l487"></a>
<span id="l488"></span><a href="#l488"></a>
<span id="l489">    <span class="c"># Gnome&#39;s Galeon and Epiphany</span></span><a href="#l489"></a>
<span id="l490">    <span class="k">for</span> <span class="n">browser</span> <span class="ow">in</span> <span class="p">(</span><span class="s">&quot;galeon&quot;</span><span class="p">,</span> <span class="s">&quot;epiphany&quot;</span><span class="p">):</span></span><a href="#l490"></a>
<span id="l491">        <span class="k">if</span> <span class="n">_iscommand</span><span class="p">(</span><span class="n">browser</span><span class="p">):</span></span><a href="#l491"></a>
<span id="l492">            <span class="n">register</span><span class="p">(</span><span class="n">browser</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">Galeon</span><span class="p">(</span><span class="n">browser</span><span class="p">))</span></span><a href="#l492"></a>
<span id="l493"></span><a href="#l493"></a>
<span id="l494">    <span class="c"># Skipstone, another Gtk/Mozilla based browser</span></span><a href="#l494"></a>
<span id="l495">    <span class="k">if</span> <span class="n">_iscommand</span><span class="p">(</span><span class="s">&quot;skipstone&quot;</span><span class="p">):</span></span><a href="#l495"></a>
<span id="l496">        <span class="n">register</span><span class="p">(</span><span class="s">&quot;skipstone&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">BackgroundBrowser</span><span class="p">(</span><span class="s">&quot;skipstone&quot;</span><span class="p">))</span></span><a href="#l496"></a>
<span id="l497"></span><a href="#l497"></a>
<span id="l498">    <span class="c"># Google Chrome/Chromium browsers</span></span><a href="#l498"></a>
<span id="l499">    <span class="k">for</span> <span class="n">browser</span> <span class="ow">in</span> <span class="p">(</span><span class="s">&quot;google-chrome&quot;</span><span class="p">,</span> <span class="s">&quot;chrome&quot;</span><span class="p">,</span> <span class="s">&quot;chromium&quot;</span><span class="p">,</span> <span class="s">&quot;chromium-browser&quot;</span><span class="p">):</span></span><a href="#l499"></a>
<span id="l500">        <span class="k">if</span> <span class="n">_iscommand</span><span class="p">(</span><span class="n">browser</span><span class="p">):</span></span><a href="#l500"></a>
<span id="l501">            <span class="n">register</span><span class="p">(</span><span class="n">browser</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">Chrome</span><span class="p">(</span><span class="n">browser</span><span class="p">))</span></span><a href="#l501"></a>
<span id="l502"></span><a href="#l502"></a>
<span id="l503">    <span class="c"># Opera, quite popular</span></span><a href="#l503"></a>
<span id="l504">    <span class="k">if</span> <span class="n">_iscommand</span><span class="p">(</span><span class="s">&quot;opera&quot;</span><span class="p">):</span></span><a href="#l504"></a>
<span id="l505">        <span class="n">register</span><span class="p">(</span><span class="s">&quot;opera&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">Opera</span><span class="p">(</span><span class="s">&quot;opera&quot;</span><span class="p">))</span></span><a href="#l505"></a>
<span id="l506"></span><a href="#l506"></a>
<span id="l507">    <span class="c"># Next, Mosaic -- old but still in use.</span></span><a href="#l507"></a>
<span id="l508">    <span class="k">if</span> <span class="n">_iscommand</span><span class="p">(</span><span class="s">&quot;mosaic&quot;</span><span class="p">):</span></span><a href="#l508"></a>
<span id="l509">        <span class="n">register</span><span class="p">(</span><span class="s">&quot;mosaic&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">BackgroundBrowser</span><span class="p">(</span><span class="s">&quot;mosaic&quot;</span><span class="p">))</span></span><a href="#l509"></a>
<span id="l510"></span><a href="#l510"></a>
<span id="l511">    <span class="c"># Grail, the Python browser. Does anybody still use it?</span></span><a href="#l511"></a>
<span id="l512">    <span class="k">if</span> <span class="n">_iscommand</span><span class="p">(</span><span class="s">&quot;grail&quot;</span><span class="p">):</span></span><a href="#l512"></a>
<span id="l513">        <span class="n">register</span><span class="p">(</span><span class="s">&quot;grail&quot;</span><span class="p">,</span> <span class="n">Grail</span><span class="p">,</span> <span class="bp">None</span><span class="p">)</span></span><a href="#l513"></a>
<span id="l514"></span><a href="#l514"></a>
<span id="l515"><span class="c"># Prefer X browsers if present</span></span><a href="#l515"></a>
<span id="l516"><span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&quot;DISPLAY&quot;</span><span class="p">):</span></span><a href="#l516"></a>
<span id="l517">    <span class="n">register_X_browsers</span><span class="p">()</span></span><a href="#l517"></a>
<span id="l518"></span><a href="#l518"></a>
<span id="l519"><span class="c"># Also try console browsers</span></span><a href="#l519"></a>
<span id="l520"><span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&quot;TERM&quot;</span><span class="p">):</span></span><a href="#l520"></a>
<span id="l521">    <span class="k">if</span> <span class="n">_iscommand</span><span class="p">(</span><span class="s">&quot;www-browser&quot;</span><span class="p">):</span></span><a href="#l521"></a>
<span id="l522">        <span class="n">register</span><span class="p">(</span><span class="s">&quot;www-browser&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">GenericBrowser</span><span class="p">(</span><span class="s">&quot;www-browser&quot;</span><span class="p">))</span></span><a href="#l522"></a>
<span id="l523">    <span class="c"># The Links/elinks browsers &lt;http://artax.karlin.mff.cuni.cz/~mikulas/links/&gt;</span></span><a href="#l523"></a>
<span id="l524">    <span class="k">if</span> <span class="n">_iscommand</span><span class="p">(</span><span class="s">&quot;links&quot;</span><span class="p">):</span></span><a href="#l524"></a>
<span id="l525">        <span class="n">register</span><span class="p">(</span><span class="s">&quot;links&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">GenericBrowser</span><span class="p">(</span><span class="s">&quot;links&quot;</span><span class="p">))</span></span><a href="#l525"></a>
<span id="l526">    <span class="k">if</span> <span class="n">_iscommand</span><span class="p">(</span><span class="s">&quot;elinks&quot;</span><span class="p">):</span></span><a href="#l526"></a>
<span id="l527">        <span class="n">register</span><span class="p">(</span><span class="s">&quot;elinks&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">Elinks</span><span class="p">(</span><span class="s">&quot;elinks&quot;</span><span class="p">))</span></span><a href="#l527"></a>
<span id="l528">    <span class="c"># The Lynx browser &lt;http://lynx.isc.org/&gt;, &lt;http://lynx.browser.org/&gt;</span></span><a href="#l528"></a>
<span id="l529">    <span class="k">if</span> <span class="n">_iscommand</span><span class="p">(</span><span class="s">&quot;lynx&quot;</span><span class="p">):</span></span><a href="#l529"></a>
<span id="l530">        <span class="n">register</span><span class="p">(</span><span class="s">&quot;lynx&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">GenericBrowser</span><span class="p">(</span><span class="s">&quot;lynx&quot;</span><span class="p">))</span></span><a href="#l530"></a>
<span id="l531">    <span class="c"># The w3m browser &lt;http://w3m.sourceforge.net/&gt;</span></span><a href="#l531"></a>
<span id="l532">    <span class="k">if</span> <span class="n">_iscommand</span><span class="p">(</span><span class="s">&quot;w3m&quot;</span><span class="p">):</span></span><a href="#l532"></a>
<span id="l533">        <span class="n">register</span><span class="p">(</span><span class="s">&quot;w3m&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">GenericBrowser</span><span class="p">(</span><span class="s">&quot;w3m&quot;</span><span class="p">))</span></span><a href="#l533"></a>
<span id="l534"></span><a href="#l534"></a>
<span id="l535"><span class="c">#</span></span><a href="#l535"></a>
<span id="l536"><span class="c"># Platform support for Windows</span></span><a href="#l536"></a>
<span id="l537"><span class="c">#</span></span><a href="#l537"></a>
<span id="l538"></span><a href="#l538"></a>
<span id="l539"><span class="k">if</span> <span class="n">sys</span><span class="o">.</span><span class="n">platform</span><span class="p">[:</span><span class="mi">3</span><span class="p">]</span> <span class="o">==</span> <span class="s">&quot;win&quot;</span><span class="p">:</span></span><a href="#l539"></a>
<span id="l540">    <span class="k">class</span> <span class="nc">WindowsDefault</span><span class="p">(</span><span class="n">BaseBrowser</span><span class="p">):</span></span><a href="#l540"></a>
<span id="l541">        <span class="k">def</span> <span class="nf">open</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">url</span><span class="p">,</span> <span class="n">new</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">autoraise</span><span class="o">=</span><span class="bp">True</span><span class="p">):</span></span><a href="#l541"></a>
<span id="l542">            <span class="k">try</span><span class="p">:</span></span><a href="#l542"></a>
<span id="l543">                <span class="n">os</span><span class="o">.</span><span class="n">startfile</span><span class="p">(</span><span class="n">url</span><span class="p">)</span></span><a href="#l543"></a>
<span id="l544">            <span class="k">except</span> <span class="ne">WindowsError</span><span class="p">:</span></span><a href="#l544"></a>
<span id="l545">                <span class="c"># [Error 22] No application is associated with the specified</span></span><a href="#l545"></a>
<span id="l546">                <span class="c"># file for this operation: &#39;&lt;URL&gt;&#39;</span></span><a href="#l546"></a>
<span id="l547">                <span class="k">return</span> <span class="bp">False</span></span><a href="#l547"></a>
<span id="l548">            <span class="k">else</span><span class="p">:</span></span><a href="#l548"></a>
<span id="l549">                <span class="k">return</span> <span class="bp">True</span></span><a href="#l549"></a>
<span id="l550"></span><a href="#l550"></a>
<span id="l551">    <span class="n">_tryorder</span> <span class="o">=</span> <span class="p">[]</span></span><a href="#l551"></a>
<span id="l552">    <span class="n">_browsers</span> <span class="o">=</span> <span class="p">{}</span></span><a href="#l552"></a>
<span id="l553"></span><a href="#l553"></a>
<span id="l554">    <span class="c"># First try to use the default Windows browser</span></span><a href="#l554"></a>
<span id="l555">    <span class="n">register</span><span class="p">(</span><span class="s">&quot;windows-default&quot;</span><span class="p">,</span> <span class="n">WindowsDefault</span><span class="p">)</span></span><a href="#l555"></a>
<span id="l556"></span><a href="#l556"></a>
<span id="l557">    <span class="c"># Detect some common Windows browsers, fallback to IE</span></span><a href="#l557"></a>
<span id="l558">    <span class="n">iexplore</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&quot;PROGRAMFILES&quot;</span><span class="p">,</span> <span class="s">&quot;C:</span><span class="se">\\</span><span class="s">Program Files&quot;</span><span class="p">),</span></span><a href="#l558"></a>
<span id="l559">                            <span class="s">&quot;Internet Explorer</span><span class="se">\\</span><span class="s">IEXPLORE.EXE&quot;</span><span class="p">)</span></span><a href="#l559"></a>
<span id="l560">    <span class="k">for</span> <span class="n">browser</span> <span class="ow">in</span> <span class="p">(</span><span class="s">&quot;firefox&quot;</span><span class="p">,</span> <span class="s">&quot;firebird&quot;</span><span class="p">,</span> <span class="s">&quot;seamonkey&quot;</span><span class="p">,</span> <span class="s">&quot;mozilla&quot;</span><span class="p">,</span></span><a href="#l560"></a>
<span id="l561">                    <span class="s">&quot;netscape&quot;</span><span class="p">,</span> <span class="s">&quot;opera&quot;</span><span class="p">,</span> <span class="n">iexplore</span><span class="p">):</span></span><a href="#l561"></a>
<span id="l562">        <span class="k">if</span> <span class="n">_iscommand</span><span class="p">(</span><span class="n">browser</span><span class="p">):</span></span><a href="#l562"></a>
<span id="l563">            <span class="n">register</span><span class="p">(</span><span class="n">browser</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">BackgroundBrowser</span><span class="p">(</span><span class="n">browser</span><span class="p">))</span></span><a href="#l563"></a>
<span id="l564"></span><a href="#l564"></a>
<span id="l565"><span class="c">#</span></span><a href="#l565"></a>
<span id="l566"><span class="c"># Platform support for MacOS</span></span><a href="#l566"></a>
<span id="l567"><span class="c">#</span></span><a href="#l567"></a>
<span id="l568"></span><a href="#l568"></a>
<span id="l569"><span class="k">if</span> <span class="n">sys</span><span class="o">.</span><span class="n">platform</span> <span class="o">==</span> <span class="s">&#39;darwin&#39;</span><span class="p">:</span></span><a href="#l569"></a>
<span id="l570">    <span class="c"># Adapted from patch submitted to SourceForge by Steven J. Burr</span></span><a href="#l570"></a>
<span id="l571">    <span class="k">class</span> <span class="nc">MacOSX</span><span class="p">(</span><span class="n">BaseBrowser</span><span class="p">):</span></span><a href="#l571"></a>
<span id="l572">        <span class="sd">&quot;&quot;&quot;Launcher class for Aqua browsers on Mac OS X</span></span><a href="#l572"></a>
<span id="l573"></span><a href="#l573"></a>
<span id="l574"><span class="sd">        Optionally specify a browser name on instantiation.  Note that this</span></span><a href="#l574"></a>
<span id="l575"><span class="sd">        will not work for Aqua browsers if the user has moved the application</span></span><a href="#l575"></a>
<span id="l576"><span class="sd">        package after installation.</span></span><a href="#l576"></a>
<span id="l577"></span><a href="#l577"></a>
<span id="l578"><span class="sd">        If no browser is specified, the default browser, as specified in the</span></span><a href="#l578"></a>
<span id="l579"><span class="sd">        Internet System Preferences panel, will be used.</span></span><a href="#l579"></a>
<span id="l580"><span class="sd">        &quot;&quot;&quot;</span></span><a href="#l580"></a>
<span id="l581">        <span class="k">def</span> <span class="nf">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">):</span></span><a href="#l581"></a>
<span id="l582">            <span class="bp">self</span><span class="o">.</span><span class="n">name</span> <span class="o">=</span> <span class="n">name</span></span><a href="#l582"></a>
<span id="l583"></span><a href="#l583"></a>
<span id="l584">        <span class="k">def</span> <span class="nf">open</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">url</span><span class="p">,</span> <span class="n">new</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">autoraise</span><span class="o">=</span><span class="bp">True</span><span class="p">):</span></span><a href="#l584"></a>
<span id="l585">            <span class="k">assert</span> <span class="s">&quot;&#39;&quot;</span> <span class="ow">not</span> <span class="ow">in</span> <span class="n">url</span></span><a href="#l585"></a>
<span id="l586">            <span class="c"># hack for local urls</span></span><a href="#l586"></a>
<span id="l587">            <span class="k">if</span> <span class="ow">not</span> <span class="s">&#39;:&#39;</span> <span class="ow">in</span> <span class="n">url</span><span class="p">:</span></span><a href="#l587"></a>
<span id="l588">                <span class="n">url</span> <span class="o">=</span> <span class="s">&#39;file:&#39;</span><span class="o">+</span><span class="n">url</span></span><a href="#l588"></a>
<span id="l589"></span><a href="#l589"></a>
<span id="l590">            <span class="c"># new must be 0 or 1</span></span><a href="#l590"></a>
<span id="l591">            <span class="n">new</span> <span class="o">=</span> <span class="nb">int</span><span class="p">(</span><span class="nb">bool</span><span class="p">(</span><span class="n">new</span><span class="p">))</span></span><a href="#l591"></a>
<span id="l592">            <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s">&quot;default&quot;</span><span class="p">:</span></span><a href="#l592"></a>
<span id="l593">                <span class="c"># User called open, open_new or get without a browser parameter</span></span><a href="#l593"></a>
<span id="l594">                <span class="n">script</span> <span class="o">=</span> <span class="s">&#39;open location &quot;</span><span class="si">%s</span><span class="s">&quot;&#39;</span> <span class="o">%</span> <span class="n">url</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="s">&#39;&quot;&#39;</span><span class="p">,</span> <span class="s">&#39;%22&#39;</span><span class="p">)</span> <span class="c"># opens in default browser</span></span><a href="#l594"></a>
<span id="l595">            <span class="k">else</span><span class="p">:</span></span><a href="#l595"></a>
<span id="l596">                <span class="c"># User called get and chose a browser</span></span><a href="#l596"></a>
<span id="l597">                <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s">&quot;OmniWeb&quot;</span><span class="p">:</span></span><a href="#l597"></a>
<span id="l598">                    <span class="n">toWindow</span> <span class="o">=</span> <span class="s">&quot;&quot;</span></span><a href="#l598"></a>
<span id="l599">                <span class="k">else</span><span class="p">:</span></span><a href="#l599"></a>
<span id="l600">                    <span class="c"># Include toWindow parameter of OpenURL command for browsers</span></span><a href="#l600"></a>
<span id="l601">                    <span class="c"># that support it.  0 == new window; -1 == existing</span></span><a href="#l601"></a>
<span id="l602">                    <span class="n">toWindow</span> <span class="o">=</span> <span class="s">&quot;toWindow </span><span class="si">%d</span><span class="s">&quot;</span> <span class="o">%</span> <span class="p">(</span><span class="n">new</span> <span class="o">-</span> <span class="mi">1</span><span class="p">)</span></span><a href="#l602"></a>
<span id="l603">                <span class="n">cmd</span> <span class="o">=</span> <span class="s">&#39;OpenURL &quot;</span><span class="si">%s</span><span class="s">&quot;&#39;</span> <span class="o">%</span> <span class="n">url</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="s">&#39;&quot;&#39;</span><span class="p">,</span> <span class="s">&#39;%22&#39;</span><span class="p">)</span></span><a href="#l603"></a>
<span id="l604">                <span class="n">script</span> <span class="o">=</span> <span class="s">&#39;&#39;&#39;tell application &quot;</span><span class="si">%s</span><span class="s">&quot;</span></span><a href="#l604"></a>
<span id="l605"><span class="s">                                activate</span></span><a href="#l605"></a>
<span id="l606"><span class="s">                                </span><span class="si">%s</span><span class="s"> </span><span class="si">%s</span><span class="s"></span></span><a href="#l606"></a>
<span id="l607"><span class="s">                            end tell&#39;&#39;&#39;</span> <span class="o">%</span> <span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">name</span><span class="p">,</span> <span class="n">cmd</span><span class="p">,</span> <span class="n">toWindow</span><span class="p">)</span></span><a href="#l607"></a>
<span id="l608">            <span class="c"># Open pipe to AppleScript through osascript command</span></span><a href="#l608"></a>
<span id="l609">            <span class="n">osapipe</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">popen</span><span class="p">(</span><span class="s">&quot;osascript&quot;</span><span class="p">,</span> <span class="s">&quot;w&quot;</span><span class="p">)</span></span><a href="#l609"></a>
<span id="l610">            <span class="k">if</span> <span class="n">osapipe</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l610"></a>
<span id="l611">                <span class="k">return</span> <span class="bp">False</span></span><a href="#l611"></a>
<span id="l612">            <span class="c"># Write script to osascript&#39;s stdin</span></span><a href="#l612"></a>
<span id="l613">            <span class="n">osapipe</span><span class="o">.</span><span class="n">write</span><span class="p">(</span><span class="n">script</span><span class="p">)</span></span><a href="#l613"></a>
<span id="l614">            <span class="n">rc</span> <span class="o">=</span> <span class="n">osapipe</span><span class="o">.</span><span class="n">close</span><span class="p">()</span></span><a href="#l614"></a>
<span id="l615">            <span class="k">return</span> <span class="ow">not</span> <span class="n">rc</span></span><a href="#l615"></a>
<span id="l616"></span><a href="#l616"></a>
<span id="l617">    <span class="k">class</span> <span class="nc">MacOSXOSAScript</span><span class="p">(</span><span class="n">BaseBrowser</span><span class="p">):</span></span><a href="#l617"></a>
<span id="l618">        <span class="k">def</span> <span class="nf">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">):</span></span><a href="#l618"></a>
<span id="l619">            <span class="bp">self</span><span class="o">.</span><span class="n">_name</span> <span class="o">=</span> <span class="n">name</span></span><a href="#l619"></a>
<span id="l620"></span><a href="#l620"></a>
<span id="l621">        <span class="k">def</span> <span class="nf">open</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">url</span><span class="p">,</span> <span class="n">new</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">autoraise</span><span class="o">=</span><span class="bp">True</span><span class="p">):</span></span><a href="#l621"></a>
<span id="l622">            <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">_name</span> <span class="o">==</span> <span class="s">&#39;default&#39;</span><span class="p">:</span></span><a href="#l622"></a>
<span id="l623">                <span class="n">script</span> <span class="o">=</span> <span class="s">&#39;open location &quot;</span><span class="si">%s</span><span class="s">&quot;&#39;</span> <span class="o">%</span> <span class="n">url</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="s">&#39;&quot;&#39;</span><span class="p">,</span> <span class="s">&#39;%22&#39;</span><span class="p">)</span> <span class="c"># opens in default browser</span></span><a href="#l623"></a>
<span id="l624">            <span class="k">else</span><span class="p">:</span></span><a href="#l624"></a>
<span id="l625">                <span class="n">script</span> <span class="o">=</span> <span class="s">&#39;&#39;&#39;</span></span><a href="#l625"></a>
<span id="l626"><span class="s">                   tell application &quot;</span><span class="si">%s</span><span class="s">&quot;</span></span><a href="#l626"></a>
<span id="l627"><span class="s">                       activate</span></span><a href="#l627"></a>
<span id="l628"><span class="s">                       open location &quot;</span><span class="si">%s</span><span class="s">&quot;</span></span><a href="#l628"></a>
<span id="l629"><span class="s">                   end</span></span><a href="#l629"></a>
<span id="l630"><span class="s">                   &#39;&#39;&#39;</span><span class="o">%</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_name</span><span class="p">,</span> <span class="n">url</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="s">&#39;&quot;&#39;</span><span class="p">,</span> <span class="s">&#39;%22&#39;</span><span class="p">))</span></span><a href="#l630"></a>
<span id="l631"></span><a href="#l631"></a>
<span id="l632">            <span class="n">osapipe</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">popen</span><span class="p">(</span><span class="s">&quot;osascript&quot;</span><span class="p">,</span> <span class="s">&quot;w&quot;</span><span class="p">)</span></span><a href="#l632"></a>
<span id="l633">            <span class="k">if</span> <span class="n">osapipe</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l633"></a>
<span id="l634">                <span class="k">return</span> <span class="bp">False</span></span><a href="#l634"></a>
<span id="l635"></span><a href="#l635"></a>
<span id="l636">            <span class="n">osapipe</span><span class="o">.</span><span class="n">write</span><span class="p">(</span><span class="n">script</span><span class="p">)</span></span><a href="#l636"></a>
<span id="l637">            <span class="n">rc</span> <span class="o">=</span> <span class="n">osapipe</span><span class="o">.</span><span class="n">close</span><span class="p">()</span></span><a href="#l637"></a>
<span id="l638">            <span class="k">return</span> <span class="ow">not</span> <span class="n">rc</span></span><a href="#l638"></a>
<span id="l639"></span><a href="#l639"></a>
<span id="l640"></span><a href="#l640"></a>
<span id="l641">    <span class="c"># Don&#39;t clear _tryorder or _browsers since OS X can use above Unix support</span></span><a href="#l641"></a>
<span id="l642">    <span class="c"># (but we prefer using the OS X specific stuff)</span></span><a href="#l642"></a>
<span id="l643">    <span class="n">register</span><span class="p">(</span><span class="s">&quot;safari&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">MacOSXOSAScript</span><span class="p">(</span><span class="s">&#39;safari&#39;</span><span class="p">),</span> <span class="o">-</span><span class="mi">1</span><span class="p">)</span></span><a href="#l643"></a>
<span id="l644">    <span class="n">register</span><span class="p">(</span><span class="s">&quot;firefox&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">MacOSXOSAScript</span><span class="p">(</span><span class="s">&#39;firefox&#39;</span><span class="p">),</span> <span class="o">-</span><span class="mi">1</span><span class="p">)</span></span><a href="#l644"></a>
<span id="l645">    <span class="n">register</span><span class="p">(</span><span class="s">&quot;MacOSX&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">MacOSXOSAScript</span><span class="p">(</span><span class="s">&#39;default&#39;</span><span class="p">),</span> <span class="o">-</span><span class="mi">1</span><span class="p">)</span></span><a href="#l645"></a>
<span id="l646"></span><a href="#l646"></a>
<span id="l647"></span><a href="#l647"></a>
<span id="l648"><span class="c">#</span></span><a href="#l648"></a>
<span id="l649"><span class="c"># Platform support for OS/2</span></span><a href="#l649"></a>
<span id="l650"><span class="c">#</span></span><a href="#l650"></a>
<span id="l651"></span><a href="#l651"></a>
<span id="l652"><span class="k">if</span> <span class="n">sys</span><span class="o">.</span><span class="n">platform</span><span class="p">[:</span><span class="mi">3</span><span class="p">]</span> <span class="o">==</span> <span class="s">&quot;os2&quot;</span> <span class="ow">and</span> <span class="n">_iscommand</span><span class="p">(</span><span class="s">&quot;netscape&quot;</span><span class="p">):</span></span><a href="#l652"></a>
<span id="l653">    <span class="n">_tryorder</span> <span class="o">=</span> <span class="p">[]</span></span><a href="#l653"></a>
<span id="l654">    <span class="n">_browsers</span> <span class="o">=</span> <span class="p">{}</span></span><a href="#l654"></a>
<span id="l655">    <span class="n">register</span><span class="p">(</span><span class="s">&quot;os2netscape&quot;</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span></span><a href="#l655"></a>
<span id="l656">             <span class="n">GenericBrowser</span><span class="p">([</span><span class="s">&quot;start&quot;</span><span class="p">,</span> <span class="s">&quot;netscape&quot;</span><span class="p">,</span> <span class="s">&quot;</span><span class="si">%s</span><span class="s">&quot;</span><span class="p">]),</span> <span class="o">-</span><span class="mi">1</span><span class="p">)</span></span><a href="#l656"></a>
<span id="l657"></span><a href="#l657"></a>
<span id="l658"></span><a href="#l658"></a>
<span id="l659"><span class="c"># OK, now that we know what the default preference orders for each</span></span><a href="#l659"></a>
<span id="l660"><span class="c"># platform are, allow user to override them with the BROWSER variable.</span></span><a href="#l660"></a>
<span id="l661"><span class="k">if</span> <span class="s">&quot;BROWSER&quot;</span> <span class="ow">in</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">:</span></span><a href="#l661"></a>
<span id="l662">    <span class="n">_userchoices</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">[</span><span class="s">&quot;BROWSER&quot;</span><span class="p">]</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">pathsep</span><span class="p">)</span></span><a href="#l662"></a>
<span id="l663">    <span class="n">_userchoices</span><span class="o">.</span><span class="n">reverse</span><span class="p">()</span></span><a href="#l663"></a>
<span id="l664"></span><a href="#l664"></a>
<span id="l665">    <span class="c"># Treat choices in same way as if passed into get() but do register</span></span><a href="#l665"></a>
<span id="l666">    <span class="c"># and prepend to _tryorder</span></span><a href="#l666"></a>
<span id="l667">    <span class="k">for</span> <span class="n">cmdline</span> <span class="ow">in</span> <span class="n">_userchoices</span><span class="p">:</span></span><a href="#l667"></a>
<span id="l668">        <span class="k">if</span> <span class="n">cmdline</span> <span class="o">!=</span> <span class="s">&#39;&#39;</span><span class="p">:</span></span><a href="#l668"></a>
<span id="l669">            <span class="n">cmd</span> <span class="o">=</span> <span class="n">_synthesize</span><span class="p">(</span><span class="n">cmdline</span><span class="p">,</span> <span class="o">-</span><span class="mi">1</span><span class="p">)</span></span><a href="#l669"></a>
<span id="l670">            <span class="k">if</span> <span class="n">cmd</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l670"></a>
<span id="l671">                <span class="n">register</span><span class="p">(</span><span class="n">cmdline</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">GenericBrowser</span><span class="p">(</span><span class="n">cmdline</span><span class="p">),</span> <span class="o">-</span><span class="mi">1</span><span class="p">)</span></span><a href="#l671"></a>
<span id="l672">    <span class="n">cmdline</span> <span class="o">=</span> <span class="bp">None</span> <span class="c"># to make del work if _userchoices was empty</span></span><a href="#l672"></a>
<span id="l673">    <span class="k">del</span> <span class="n">cmdline</span></span><a href="#l673"></a>
<span id="l674">    <span class="k">del</span> <span class="n">_userchoices</span></span><a href="#l674"></a>
<span id="l675"></span><a href="#l675"></a>
<span id="l676"><span class="c"># what to do if _tryorder is now empty?</span></span><a href="#l676"></a>
<span id="l677"></span><a href="#l677"></a>
<span id="l678"></span><a href="#l678"></a>
<span id="l679"><span class="k">def</span> <span class="nf">main</span><span class="p">():</span></span><a href="#l679"></a>
<span id="l680">    <span class="kn">import</span> <span class="nn">getopt</span></span><a href="#l680"></a>
<span id="l681">    <span class="n">usage</span> <span class="o">=</span> <span class="s">&quot;&quot;&quot;Usage: </span><span class="si">%s</span><span class="s"> [-n | -t] url</span></span><a href="#l681"></a>
<span id="l682"><span class="s">    -n: open new window</span></span><a href="#l682"></a>
<span id="l683"><span class="s">    -t: open new tab&quot;&quot;&quot;</span> <span class="o">%</span> <span class="n">sys</span><span class="o">.</span><span class="n">argv</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span></span><a href="#l683"></a>
<span id="l684">    <span class="k">try</span><span class="p">:</span></span><a href="#l684"></a>
<span id="l685">        <span class="n">opts</span><span class="p">,</span> <span class="n">args</span> <span class="o">=</span> <span class="n">getopt</span><span class="o">.</span><span class="n">getopt</span><span class="p">(</span><span class="n">sys</span><span class="o">.</span><span class="n">argv</span><span class="p">[</span><span class="mi">1</span><span class="p">:],</span> <span class="s">&#39;ntd&#39;</span><span class="p">)</span></span><a href="#l685"></a>
<span id="l686">    <span class="k">except</span> <span class="n">getopt</span><span class="o">.</span><span class="n">error</span><span class="p">,</span> <span class="n">msg</span><span class="p">:</span></span><a href="#l686"></a>
<span id="l687">        <span class="k">print</span> <span class="o">&gt;&gt;</span><span class="n">sys</span><span class="o">.</span><span class="n">stderr</span><span class="p">,</span> <span class="n">msg</span></span><a href="#l687"></a>
<span id="l688">        <span class="k">print</span> <span class="o">&gt;&gt;</span><span class="n">sys</span><span class="o">.</span><span class="n">stderr</span><span class="p">,</span> <span class="n">usage</span></span><a href="#l688"></a>
<span id="l689">        <span class="n">sys</span><span class="o">.</span><span class="n">exit</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span></span><a href="#l689"></a>
<span id="l690">    <span class="n">new_win</span> <span class="o">=</span> <span class="mi">0</span></span><a href="#l690"></a>
<span id="l691">    <span class="k">for</span> <span class="n">o</span><span class="p">,</span> <span class="n">a</span> <span class="ow">in</span> <span class="n">opts</span><span class="p">:</span></span><a href="#l691"></a>
<span id="l692">        <span class="k">if</span> <span class="n">o</span> <span class="o">==</span> <span class="s">&#39;-n&#39;</span><span class="p">:</span> <span class="n">new_win</span> <span class="o">=</span> <span class="mi">1</span></span><a href="#l692"></a>
<span id="l693">        <span class="k">elif</span> <span class="n">o</span> <span class="o">==</span> <span class="s">&#39;-t&#39;</span><span class="p">:</span> <span class="n">new_win</span> <span class="o">=</span> <span class="mi">2</span></span><a href="#l693"></a>
<span id="l694">    <span class="k">if</span> <span class="nb">len</span><span class="p">(</span><span class="n">args</span><span class="p">)</span> <span class="o">!=</span> <span class="mi">1</span><span class="p">:</span></span><a href="#l694"></a>
<span id="l695">        <span class="k">print</span> <span class="o">&gt;&gt;</span><span class="n">sys</span><span class="o">.</span><span class="n">stderr</span><span class="p">,</span> <span class="n">usage</span></span><a href="#l695"></a>
<span id="l696">        <span class="n">sys</span><span class="o">.</span><span class="n">exit</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span></span><a href="#l696"></a>
<span id="l697"></span><a href="#l697"></a>
<span id="l698">    <span class="n">url</span> <span class="o">=</span> <span class="n">args</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span></span><a href="#l698"></a>
<span id="l699">    <span class="nb">open</span><span class="p">(</span><span class="n">url</span><span class="p">,</span> <span class="n">new_win</span><span class="p">)</span></span><a href="#l699"></a>
<span id="l700"></span><a href="#l700"></a>
<span id="l701">    <span class="k">print</span> <span class="s">&quot;</span><span class="se">\a</span><span class="s">&quot;</span></span><a href="#l701"></a>
<span id="l702"></span><a href="#l702"></a>
<span id="l703"><span class="k">if</span> <span class="n">__name__</span> <span class="o">==</span> <span class="s">&quot;__main__&quot;</span><span class="p">:</span></span><a href="#l703"></a>
<span id="l704">    <span class="n">main</span><span class="p">()</span></span><a href="#l704"></a></pre>
<div class="sourcelast"></div>
</div>
</div>
</div>

<script type="text/javascript">process_dates()</script>


</body>
</html>

